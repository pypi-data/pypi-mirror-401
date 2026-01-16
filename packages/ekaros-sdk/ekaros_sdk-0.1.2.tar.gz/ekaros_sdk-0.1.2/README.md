# Ekaros SDK

Ekaros Python SDK is the Python SDK to implement Ekaros Experiments on Python applications.

## Features

- **Performance Monitoring**: Track API latency, memory usage, and response metrics
- **A/B Journeys Testing**: Run experiments with multiple variations
- **Comprehensive Metrics**: Capture request/response data, headers, and custom parameters
- **Asynchronous Tracking**: Non-blocking metrics collection

## Supports

- Django

## Installation

```bash
pip install ekaros-sdk
```

## Quick Start

### 1. Initialize Ekaros in your Django project

In your Django `urls.py`:

```python
from django.urls import path, include
from ekaros import Ekaros

# Initialize Ekaros with your SDK key
ekaros_instance = Ekaros(
    framework="django",
    sdk_key="your-sdk-key-here"
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),
    # Include Ekaros URLs
    path('ekaros/', include(('ekaros.backends.django.urls', 'ekaros'), namespace='ekaros')),
]

# Load URL patterns into Ekaros
ekaros_instance.load_url_patterns(urlpatterns)

# Override with Ekaros-enhanced patterns
urlpatterns = ekaros_instance.get_urlpatterns()
```

### 2. Register Views for A/B Testing

All your existsing views in the urls will be automatically registered. If you want to register new Views, you can use:

```python
@ekaros.register(name="my_app:checkout_view")
def checkout_view_v1(request):
    return render(request, 'checkout_v1.html')

@ekaros.register(name="my_app:checkout_view")
def checkout_view_v2(request):
    return render(request, 'checkout_v2.html')

@ekaros.register(name="ab_apis:simple_view")
class SimpleButtonView(View):
   def get(self, request):
       return JsonResponse({"response_data": "GET API from Simple View"})


   def post(self, request):
       return JsonResponse({"response_data": "POST API from Simple View"})
```

## Configuration Options

When initializing Ekaros, you can pass the following options:

```python
ekaros = Ekaros(
    framework="django",
    sdk_key="your-sdk-key",
    instance_name="default",  # For multiple instances
    # Additional backend-specific options
)
```

## Advanced Features

### Client Token Generation

Generate tokens for client-side tracking:

```python
token = ekaros.create_client_token(
    custom_parameters={"user_id": "123"},
    timeout=86400  # 24 hours
)
```

## Metrics Collected

The SDK automatically tracks:

- **Performance**: Latency, memory allocation, peak memory
- **Request Data**: Headers, body, query parameters, method, path
- **Response Data**: Headers, body, status code, content type
- **Experiment Data**: A/B test variants, journey paths
- **Error Tracking**: Exception messages and stack traces

## Requirements

- Python >= 3.8
- Django >= 5.0
- requests >= 2.25.0

## Development

### Install Development Dependencies

```bash
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Formatting

```bash
black ekaros/
flake8 ekaros/
```

## Support

For issues, questions, or contributions:

- GitHub Issues: https://github.com/Anirudh-RV/ekaros-sdk-python/issues
- Documentation: https://ekaros.dev/documentation/human/sdk/python/

## License

MIT License - see LICENSE file for details

## Changelog

### 0.1.0 (2025-01-01)

- Initial release
- Django backend support
- Performance tracking
- A/B testing capabilities
- Dynamic routing

### 0.1.1 (2025-01-01)

- Shifting all names from Discerance to Ekaros

### 0.1.2 (2025-15-01)

- Continuing journey is an error occurs
