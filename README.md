# DDNS Client
Dynamic DNS Client for several domain providers

## Supported Providers
- [x] [Cloudflare](https://www.cloudflare.com/)
- [ ] [DuckDNS](https://www.duckdns.org/)
- [ ] [Dynu](https://www.dynu.com/)
- [ ] [Namecheap](https://www.namecheap.com/)
- [ ] [No-IP](https://www.noip.com/)
- [ ] [OVH](https://www.ovh.com/)
- [ ] [Google Domains](https://domains.google.com/)

## Usage
To use this DDNS client you need to modify the `config.json` file with your credentials and the domain you want to update.

> *__NOTE__*:
>
> Currently only Cloudflare is supported. This project will be updated when our client needs to update another domain provider. if you would like to contribute, please feel free to open a pull request.

## Configuration

### Cloudflare
To use Cloudflare you need to create an API Token with the following permissions:
- Zone:Zone:Read
- Zone:DNS:Edit

You will then want to edit `config.json`, a sample is provided below:
```json
[
    {
        "domain": "vpn.example.com",
        "provider": "cloudflare",
        "api_key": "123456789",
        "record_type": "A"
    }
]
```

You can add as many domains as you want to the `config.json` file, just make sure to add a comma after the closing curly bracket `}` of the previous domain.

## Docker

> *__NOTE__*: This is not yet implemented and will be added in the future.


