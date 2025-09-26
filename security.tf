resource "aws_api_gateway_api_key" "key1" {
  name        = "key1"
  description = "API key for example API"
  enabled     = true
    value       = "12345678901234567890"
}

resource "aws_api_gateway_usage_plan" "usage1" {
  name        = "usage1"
  description = "Usage plan for example API"
  api_stages {
    api_id = aws_api_gateway_rest_api.ms1-api.id
    stage  = aws_api_gateway_stage.ms1-api-stage.stage_name
  }
  quota_settings {
    limit  = 10
    period = "DAY"
  }

  throttle_settings {
    burst_limit = 5
    rate_limit  = 10
  }
}

resource "aws_api_gateway_usage_plan_key" "usage1-key1" {
  key_id        = aws_api_gateway_api_key.key1.id
  key_type      = "API_KEY"
  usage_plan_id = aws_api_gateway_usage_plan.usage1.id
}


