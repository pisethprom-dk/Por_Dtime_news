from filer.utils.files import get_valid_filename
import os 
 
def generate_filename_by_folder(instance, filename):
    filename = instance.name or filename
    folder_part = ''
    folders = []
    folder = instance.folder
    if folder:
        while folder:
            folders.append(folder.name)
            folder = folder.parent
        folders.reverse()
        folder_part = '/'.join(folders)
        
        # check file for sub folder storage - [ image or video ]
        # file_type = filename.split('.')[1]
        # if file_type in ['dv', 'mov', 'mp4', 'avi', 'ywmv',]:
        #     folder_part = folder_part +'/videos'
        # else:
        #     folder_part = folder_part +'/images'
            
    return os.path.join(folder_part, get_valid_filename(filename))
