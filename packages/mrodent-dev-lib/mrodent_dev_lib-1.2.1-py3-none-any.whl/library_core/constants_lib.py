import logging
logging.basicConfig(format='%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
        datefmt='%H:%M:%S', level=logging.DEBUG)
# logging.basicConfig(format='line %(lineno)d ============> %(message)s',
#         datefmt='%H:%M:%S', level=logging.DEBUG)
basic_logger = logging.getLogger('BASIC')
basic_logger.info(f'start {__file__}')

import pathlib, sys, os

# get project name
cwd_path = pathlib.Path.cwd()
r"""
2025-12-28 typically found when lib (mrodent-dev-lib) is a pip-installed module:
__file__ |D:\apps\Python\virtual_envs\dev_doc_indexer\lib\site-packages\library_core\constants.py|
cwd_path |D:\My documents\software projects\EclipseWorkspace\doc_indexer|
"""
# get type of run
cwd_path_parts = cwd_path.parts
# determined_run_type = False
IS_PRODUCTION = None
run_type_index = -1
n_path_parts = len(cwd_path_parts)
for i, part in enumerate(cwd_path_parts):
  part_lc = part.lower()
  if part_lc == 'operative':
    # if being run from the project dir, "operative" must be the penultimate path part
    if i != n_path_parts - 2:
      basic_logger.error(f'FATAL. "operative" was found, but not as the penultimate CWD path part: {cwd_path_parts}')
      sys.exit()
    IS_PRODUCTION = True
    break
# NB this test is needed to stop the value of "i" increasing if IS_PRODUCTION is now True
if IS_PRODUCTION is None:
  for i, part in enumerate(cwd_path_parts):
    part_lc = part.lower()
    if 'workspace' in part_lc:
      # if being run from the project dir, "workspace" must be the penultimate path part
      if i != n_path_parts - 2:
        basic_logger.error(f'FATAL. a Path part containing "workspace" was found, but not as the penultimate CWD path part: {cwd_path_parts}')
        sys.exit()
      IS_PRODUCTION = False
      break
if IS_PRODUCTION is None:
  basic_logger.error(f'FATAL. {__file__}. Neither "operative" nor "workspace" found in CWD path parts: {cwd_path_parts}')
  sys.exit()

if not IS_PRODUCTION:
  basic_logger.info(f'--- this is a DEV run of file {__file__}')

basic_logger.info(f'+++ cwd_path_parts {cwd_path_parts} - i {i}')  

# the root directory (and thus project name will be the directory after the "operative" or "workspace" directory)
# and always as the final path part of CWD...
PROJECT_NAME = cwd_path_parts[-1]

# get PART2 env var value
PART2_NAME = 'PART2'
PART2_VAL = os.environ.get(PART2_NAME)
if PART2_VAL == None:
  basic_logger.error(f'FATAL. Environment variable |{PART2_NAME}| not set')
  sys.exit()

# get OS
lc_os_name = sys.platform.lower()
IS_LINUX = None
if lc_os_name.startswith('lin'):
  IS_LINUX = True
elif lc_os_name.startswith('win'):
  IS_LINUX = False
if IS_LINUX == None:
  basic_logger.error(f'FATAL. Cannot operate in OS {sys.platform}')
  sys.exit()
