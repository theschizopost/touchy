import argparse
import os
import time
from datetime import datetime
import yaml
import fnmatch
import logging

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.load(f, Loader=yaml.SafeLoader)

def process_content(content, filename, dirname):
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    content = content.replace('{{isotimestamp}}', timestamp)
    content = content.replace('{{filename}}', filename)
    content = content.replace('{{dirname}}', dirname)
    return content


def main():
    parser = argparse.ArgumentParser(description="Advanced touch command")
    parser.add_argument("--version", action="version", version="0.0.1")
    parser.add_argument("filename", help="filename")
    # parser.add_argument("-a", default=False, action="store_true", help="Change only the access time")
    # parser.add_argument("-c", "--no-create", default=False, action="store_true", help="Do not create any files")
    # parser.add_argument("-d", "--date", help="Use date instead of current time")
    # TODO 100% backward compatibility issue with help -h
    # parser.add_argument("--help", default=False, action="store_true", help="Print help information")
    # parser.add_argument("-h", "--no-dereference", default=False, action="store_true", help="Affect each symbolic link instead of any referenced file (useful only on systems that can change the timestamps of a symlink)")
    # parser.add_argument("-m", default=False, action="store_true", help="Change only the modification time")
    # parser.add_argument("-r", "--reference", help="Use this file's times instead of current time")
    # parser.add_argument("--time", help="Specify which time to change (-a):access/atime/use | modification time (-m): modify/mtime")

    parser.add_argument("--config", default="~/.touchy")
    parser.add_argument("--verbose", default=False, action="store_true")

    args = parser.parse_args()

    config = load_config(os.path.expanduser(args.config))
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if args.verbose or config['verbose']: logging.basicConfig(level=logging.DEBUG, format=format)
    else: logging.basicConfig(level=logging.INFO, format=format)

    file_path = os.path.expanduser(os.path.dirname(args.filename))
    if file_path=="." or file_path=="":
        file_path=os.getcwd()

    filename = os.path.basename(args.filename)
    dirname = os.path.split(file_path)[1]
    file_ext = os.path.splitext(args.filename)[1]
    logging.debug(f"filepath: {file_path}, dirname:{dirname}, filename:{filename}, file extension:{file_ext}")


    for path in config['paths']:
        if fnmatch.fnmatch(file_path, path):
            content_exts =  config['paths'][path]
        # paths = config['paths']
        # #TODO
        # if file_path in paths:
        #     content_exts = paths[file_path]
        else:
            content_exts = config['paths']['default']
    logging.debug((content_exts, type(content_exts)))

    content = ""
    for ext in content_exts:
        if fnmatch.fnmatch(filename, ext['filename']):
            content = ext['content']

    content = process_content(content, filename, dirname)
    
    atime = time.time()
    mtime = time.time()

    if args.date:
        #TODO parse date from argument
        # atime = 
        # mtime = 
        pass

    if not os.path.exists(args.filename):
        with open(args.filename, 'w') as f:
            if content:
                f.write(content)
                pass
    else:
        logging.info("File already exists, updating filename")
        os.utime(args.filename, times=(atime, mtime))

if __name__=="__main__":
    main()