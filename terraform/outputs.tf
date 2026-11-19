output "service_url" {
  description = "Service URL to check from the host and a second machine on the team network."
  value       = "http://${var.bind_address}:${var.host_port}/"
}

output "image_id" {
  description = "Immutable local image ID selected for this deployment."
  value       = var.image_id
}
