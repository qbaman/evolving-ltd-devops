variable "image_id" {
  description = "Full ID of an already-built image on the test host."
  type        = string

  validation {
    condition     = can(regex("^sha256:[0-9a-f]{64}$", var.image_id))
    error_message = "Use the full sha256 image ID returned by docker image inspect."
  }
}

variable "bind_address" {
  description = "IPv4 address of the test host interface reachable from the team's network."
  type        = string

  validation {
    condition     = can(cidrnetmask("${var.bind_address}/32")) && var.bind_address != "0.0.0.0" && !startswith(var.bind_address, "127.")
    error_message = "Use a specific non-loopback IPv4 address assigned to the test host."
  }
}

variable "host_port" {
  description = "TCP port exposed on the shared test host."
  type        = number
  default     = 8080

  validation {
    condition     = var.host_port == floor(var.host_port) && var.host_port >= 1 && var.host_port <= 65535
    error_message = "Use an integer port between 1 and 65535."
  }
}
