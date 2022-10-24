import sys

from boto3 import client


def cleanup_repository():
    """Remove any image that isn't tagged 'latest' from ECR.
    """
    ecr_client = client('ecr',
                        aws_access_key_id=sys.argv[0],
                        aws_secret_access_key=sys.argv[1],
                        region_name=sys.argv[2],
                        )

    all_images = ecr_client.list_images(repositoryName='normconf-goodies')

    old_images = [image for image in all_images['imageIds'] if not image['imageTag'].endswith('latest')]

    response2 = ecr_client.batch_delete_image(repositoryName='normconf-goodies', imageIds=old_images)

    print(response2)

if __name__ == '__main__':
    cleanup_repository()
