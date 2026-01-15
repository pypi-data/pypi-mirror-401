from cp_manage.utilities import CPVConfig, ModelsCheckpointsManage, setup_file_logging
import os
from pathlib import Path

# Setup logging to .cpv.log in current directory
log_file = Path.cwd() / ".cpv.log"
setup_file_logging(log_file)

config= CPVConfig()
# credential_path = "~/.aws/credentials"
# # aws_profile  = ec2-dev
# config.setup_aws_profile(credential_path="~/.aws/credentials", aws_profile="aws-dev", verbose=True,dry_run=False)
# config._load_config()
# config.validate_credentials(verbose=True)
# # print("AWS Profile setup completed.")
# # config.validate_credentials(verbose=True)
# # print("="*10)
# model_name = os.path.basename(os.getcwd())
mcm = ModelsCheckpointsManage(team_name="AI-Mani",model_name="gr001-1B", dry_run=False)
# mcm._create_local_structure(dry_run=False)
# # repo_path = "/home/annd/test_models_cpv/TestModel"
# # os.chdir(str(repo_path))
# # print(os.getcwd())
# # local_path="/home/annd/test_models_cpv"
# mcm.import_model_init(verbose=True, force = True)
# # mcm.write_log_file(log_file=".cpv.log", verbose=True)
# mcm.upload_model_checkpoint(dry_run=False, verbose=True)
config.is_bitbucket_configured()
config.validate_credentials(verbose=True)

mcm.upload_model_checkpoint(dry_run=False, verbose=True)
print(mcm.get_model_metadata(verbose=True))