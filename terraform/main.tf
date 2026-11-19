terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_container" "service" {
  name    = "evolving-ltd-test"
  image   = var.image_id
  restart = "unless-stopped"

  ports {
    ip       = var.bind_address
    internal = 80
    external = var.host_port
  }
}
