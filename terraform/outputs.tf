output "service_url" {
  description = "URL to check from the test host or a machine that can reach it."
  value       = "http://localhost:${var.host_port}/"
}

output "image_tag" {
  description = "Image version used by the current Terraform deployment."
  value       = var.image_tag
}
