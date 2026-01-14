from cp_manage.utilities import CPVConfig, ModelsCheckpointsManage
import os
config= CPVConfig()
credential_path = "~/.aws/credentials"
# aws_profile  = ec2-dev
config.setup_aws_profile(credential_path="~/.aws/credentials", aws_profile="aws-dev", verbose=True,dry_run=False)
# print("AWS Profile setup completed.")
# config.validate_credentials(verbose=True)
print("="*10)
model_name = os.path.basename(os.getcwd())
mcm = ModelsCheckpointsManage(team_name="TestTeam4",model_name=model_name, dry_run=False)
mcm._create_local_structure(dry_run=False)
# repo_path = "/home/annd/test_models_cpv/TestModel"
# os.chdir(str(repo_path))
# print(os.getcwd())
# local_path="/home/annd/test_models_cpv"
mcm.import_model_init(verbose=True, force = True)

# mcm.upload_model_checkpoint(dry_run=False, verbose=True)