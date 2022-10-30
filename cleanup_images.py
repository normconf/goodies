import sys

from boto3 import client


def cleanup_repository():
    """Remove any image that isn't tagged 'latest' from ECR."""
    ecr_client = client(
        "ecr",
        aws_access_key_id=sys.argv[0],
        aws_secret_access_key=sys.argv[1],
        region_name=sys.argv[2],
    )

    all_images = ecr_client.list_images(repositoryName="normconf-goodies")

    # Go through every image, only the latest should have a tag, so grab all those without imageTag and get SHA
    old_images = [image for image in all_images["imageIds"] if not image.get("imageTag")]

    ecr_client.batch_delete_image(repositoryName="normconf-goodies", imageIds=old_images)

    refresh_image_list = ecr_client.list_images(repositoryName="normconf-goodies")

    print(
        f"There are {len([image for image in refresh_image_list['imageIds'] if not image.get('imageTag')])} old images left"
    )
