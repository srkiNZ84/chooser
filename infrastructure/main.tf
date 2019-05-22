provider "google" {
  project = "faas-helloworld"
  region  = "asia-east2"
  zone    = "asia-east2-a"
}

data "archive_file" "function_archive_file" {
  type = "zip"
  source_dir = "../src"
  output_path = "function-${formatdate("YYYYMMDD-hhmm",timestamp())}.zip"
}
resource "google_storage_bucket" "chooser_functions_bucket" {
  name = "chooser-functions-bucket"
  project = "faas-helloworld"
}

resource "google_storage_bucket_object" "function_archive" {
  name   = "index-${formatdate("YYYYMMDD-hhmm",timestamp())}.zip"
  bucket = "${google_storage_bucket.chooser_functions_bucket.name}"
  source = "${data.archive_file.function_archive_file.output_path}"
}

resource "google_cloudfunctions_function" "chooser_function" {
  name                  = "functionchooser"
  description           = "Main function for Chooser blog engine"
  available_memory_mb   = 128
  source_archive_bucket = "${google_storage_bucket.chooser_functions_bucket.name}"
  source_archive_object = "${google_storage_bucket_object.function_archive.name}"
  trigger_http          = true
  timeout               = 60
  runtime               = "python37"
  entry_point           = "getposts"
  labels = {
    function = "blog-engine"
  }
}

output "function_url" {
  value = "${google_cloudfunctions_function.chooser_function.https_trigger_url}"
}
