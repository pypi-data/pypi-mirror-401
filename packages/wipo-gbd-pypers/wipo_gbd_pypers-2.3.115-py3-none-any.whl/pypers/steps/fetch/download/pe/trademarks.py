import os
import time
import io
import paramiko
import stat
#from pypers.steps.base.fetch_step import FetchStep
from pypers.steps.fetch.download.sftp_pk import SFTP_PK
from zipfile import ZipFile
import xml.dom.minidom as md

"""
This is modified version of the WIPO SFTP download for Peru, which includes a re-packaging
to ensure we have image archives that match the metadata archives
"""

class SFTP_PK_PE(SFTP_PK):
    spec = {
        "version": "2.0",
        "descr": [
            "Fetch Peru archives from either a local dir or SFTP server"
        ],
        "args":
        {
            "params": [
                {
                    "name": "sleep_secs",
                    "type": "int",
                    "descr": "secs to sleep to check if SSH dir is hot",
                    "value": 5
                }
            ],
        }
    }

    def sftp_walk(self, sftp, remotepath, folder_types):
        """
        Usual type value are "datos" or "imagenes"
        """
        path = remotepath
        files = []
        for folder in folder_types:
            new_path = os.path.join(remotepath, folder)
            for f in sftp.listdir_attr(new_path):
                files.append(f.filename)
        if files:
            yield new_path, files

    def specific_process(self):
        self.output_files = []
        sftp = self.connect()

        sftp_dir = self.sftp_params['sftp_dir']
        self.logger.info('going to dir %s' % sftp_dir)
        sftp.chdir(sftp_dir)

        print(sftp_dir)

        # metadata archive files
        flist = []
        # looks for files recursively
        for path, files in self.sftp_walk(sftp, sftp_dir, ["datos"]):
            print(path)
            for f in files:
                if self.rgx.match(f):
                    flist.append(os.path.join(path, f))

        # image archive files
        ilist = []
        for path, files in self.sftp_walk(sftp, sftp_dir, ["imagenes"]):
            print(path)
            for f in files:
                if self.rgx.match(f):
                    ilist.append(os.path.join(path, f))

        # look for directories where files are present
        upload_dirs = [os.path.dirname(os.path.relpath(f, sftp_dir))
                       for f in flist]
        # check if uploading is still active on every upload dir
        for upload_dir in set(upload_dirs):
            size_1 = sftp.stat(upload_dir).st_mtime
            time.sleep(self.sleep_secs)
            size_2 = sftp.stat(upload_dir).st_mtime

            if size_1 != size_2:
                sftp.close()
                self.ssh.close()
                raise Exception(
                    'SSH folder [%s] is HOT. Exit.' % os.path.join(sftp_dir,
                                                                   upload_dir))

            self.logger.info('SSH folder [%s] is cold' % os.path.join(
                sftp_dir, upload_dir))

        self.logger.info('get the files')

        count = 0
        reversed = True
        prefix_dates = []
        if self.limit:
            reversed = False
        for f in sorted(flist, reverse=reversed):
            filename = os.path.basename(f)  # 123.zip
            filepath = os.path.relpath(f, sftp_dir)  # dir/123.zip

            if self.limit and count == self.limit:
                break
            if filepath in self.done_archives:
                continue

            count += 1
            self.logger.info('[sftp][metadata] %s: %s' % (count, f))

            dest_dir = os.path.join(self.output_dir)
            dest_file = os.path.join(dest_dir, filename)

            try:
                os.makedirs(dest_dir, exist_ok=True)
            except Exception as e:
                raise Exception('SFTP, Failed to create destination directory: [%s]' % dest_dir)

            try:
                sftp.get(f, dest_file)
                self.output_files.append(dest_file)
                print("downloaded: " + dest_file)
                ind = filename.find("-PE")
                if ind != -1:
                    if filename[:ind] not in prefix_dates:
                        prefix_dates.append(filename[:ind])
            except Exception as e:
                raise Exception('SFTP, Failed to download: [%s]' % dest_file)
        
        print(prefix_dates)

        # download all the image files with date prefix included in the downloaded metadat files
        img_archive_files = []
        # the following map an image archive filename to the list of contained files, without date prefix
        img_archive_map = {}
        for f in ilist:
            filename = os.path.basename(f)  # 123.zip
            filepath = os.path.relpath(f, sftp_dir)  # dir/123.zip

            if len(img_archive_files)>350:
                break

            if filepath in self.done_archives:
                continue

            valid_archive = False
            # check that the prefix is useful for the metadata files
            """
            for prefix in prefix_dates:
                if filename.startswith(prefix):
                    valid_archive = True
                    break
        
            if not valid_archive:
                continue
            """
            self.logger.info('[sftp][images] %s' % f)

            dest_dir = os.path.join(self.output_dir, "imagenes")
            dest_file = os.path.join(dest_dir, filename)

            try:
                os.makedirs(dest_dir, exist_ok=True)
            except Exception as e:
                raise Exception('SFTP, Failed to create destination directory: [%s]' % dest_dir)

            try:
                sftp.get(f, dest_file)
                img_archive_files.append(dest_file)
                list_image_files = []
                with ZipFile(dest_file) as zipf:
                    for local_image_file in zipf.namelist():
                        # remove prefix
                        ind = local_image_file.find("PE50")
                        if ind != -1:
                            local_image_file = local_image_file[ind:]
                        list_image_files.append(local_image_file)
                img_archive_map[dest_file] = list_image_files
                print("downloaded: " + dest_file)
            except Exception as e:
                raise Exception('SFTP, Failed to download: [%s]' % dest_file)

        sftp.close()
        self.ssh.close()

        # repackage the images to match metadata archive numbering
        for metadata_file in self.output_files:
            image_files = []
            # get the required image files
            #print(metadata_file)
            trdmrk_imgs = []
            with ZipFile(metadata_file) as zf:
                for file in zf.namelist():
                    #print(file)
                    if not file.endswith('.xml'): 
                        continue
                    xml_text = ""
                    with io.TextIOWrapper(zf.open(file), encoding="utf-8") as f:
                        #xml_dom = md.parse(f)
                        xml_text = f.read()
                    if len(xml_text.strip()) < 5:
                        continue
                    xml_dom =  md.parseString(xml_text)
                    trdmrk_imgs += xml_dom.getElementsByTagName('MarkImageFilename')

            if len(trdmrk_imgs)>0:
                # build an image archive corresponding to this metadata archive so that it will be joined in the group/join steps
                dest_dir = os.path.join(self.output_dir)
                image_dest_file = metadata_file.replace("-DIFF-", "-DIFF(IMGA)-")
                dest_image_file = os.path.join(dest_dir, image_dest_file)
                #print(dest_image_file)

                # extract required image files and populate the the image archive
                with ZipFile(dest_image_file, 'w') as zipped_image_f:
                    for trdmrk_img in trdmrk_imgs:
                        local_filename = trdmrk_img.firstChild.nodeValue
                        # need some massage to match the actual filename in archive
                        dest_image_filename = os.path.basename(dest_image_file) 
                        ind = dest_image_filename.find("-PE")
                        if ind != -1:
                            prefix = dest_image_filename[:ind]
                        full_local_filename = prefix + "-" + local_filename
                        
                        #print(local_filename)

                        for img_archive_file in img_archive_files:
                            # try to access the image 
                            try:
                                #print("test with "+img_archive_file)
                                if local_filename in img_archive_map[img_archive_file]:
                                    #print("found local_filename in archive " + img_archive_file)
                                    with ZipFile(img_archive_file) as zipf:
                                        #print(zipf.namelist())
                                        #if local_filename in zipf.namelist():    
                                        with zipf.open(full_local_filename) as imgf:
                                            zipped_image_f.writestr(full_local_filename, imgf.read())
                                    break
                            except:
                                pass
                self.output_files.append(dest_image_file)
