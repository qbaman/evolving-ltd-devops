variable "image_tag" {
  description = "Unique image tag for this deployment. Use a commit SHA so a known-good version can be restored."
  type        = string
  default     = "local"
}

variable "host_port" {
  description = "TCP port exposed by the test host."
  type        = number
  default     = 8080
}
