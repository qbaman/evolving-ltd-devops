mock_provider "docker" {}

variables {
  bind_address = "192.0.2.10"
  host_port    = 9080
}

run "deploy" {
  command = apply

  variables {
    image_id = "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }

  assert {
    condition     = output.service_url == "http://192.0.2.10:9080/"
    error_message = "The service URL must use the configured team-facing endpoint."
  }
}

run "rollback" {
  command = plan

  variables {
    image_id = "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  }

  assert {
    condition     = docker_container.service.image == var.image_id && output.image_id != run.deploy.image_id
    error_message = "Rollback must select the requested retained image ID."
  }

  assert {
    condition = (
      docker_container.service.name == "evolving-ltd-test" &&
      one(docker_container.service.ports).ip == var.bind_address &&
      one(docker_container.service.ports).external == var.host_port &&
      one(docker_container.service.ports).internal == 80 &&
      output.service_url == run.deploy.service_url
    )
    error_message = "Rollback must preserve the configured team-facing address and ports."
  }
}
