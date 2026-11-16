terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_image" "service" {
  name         = "evolving-ltd-demo:${var.image_tag}"
  keep_locally = true

  build {
    context = "${path.module}/.."
    tag     = ["evolving-ltd-demo:${var.image_tag}"]
  }
}

resource "docker_container" "service" {
  name    = "evolving-ltd-test"
  image   = docker_image.service.image_id
  restart = "unless-stopped"

  ports {
    internal = 80
    external = var.host_port
  }
}
