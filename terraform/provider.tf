terraform {
  required_providers {
    aws={
        source = "hashicorp/aws"

    }
      random = {
      source  = "hashicorp/random"
      version = "3.4.3"
    }
  }
}
provider "aws" {
  profile = "Devops_SDE-835456546890"
  region = "ap-south-1"
}