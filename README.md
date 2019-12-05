# universal-proxy-pac

## Abstract

Sometimes you need to proxy the http(s)-traffic of specific app when you do its debugging or pentesting.  

Setting the OS-wide global proxy isn't convenient sometimes because global proxy could break some system component functionality. For instance, if you need to proxy the traffic of some iOS app, you will notice that the only option you have is to set global iOS-wide proxy. However, doing this will break many iOS components. You will be even unable to run an app you are developing because the iOS needs to communicate with the Apple servers to check the code sign, and it uses the certificate pinning there.

The only way to solve this really painlessly is to use Proxy Auto Configuration (PAC) – a protocol of dynamic proxy setting. In this case, you can specify not a static system-wide proxy, but a URL, where the specifically crafted PAC-file is located. This file contains a JS-function, which will be evaluated by browser's or any other app's low-level HTTP-library before doing every HTTP-request. This function gets current requested URL and host and should return the proxy address for them. And, depending on the function result, the proxy for this request will (or won't) be set to some host and port. Thus, you can proxy only specific hosts traffic using PAC, the interaction with every other hosts will be performed directly.

However, the PAC-file is not something you will be glad to write by hand, especially if you need to cover a lot of hosts. And that's why I've made this tiny tool to help you.

It's implemented in both Python and PHP so you can use an implementation that's more convenient for you.

## Usage

Clone a project to a server which is accessible by the device, where the proxied app is located.
Redact the `rules.json` file in a following way:
```json
{
  "127.0.0.1:8080": [
    "*.google.com",
    "facebook.com"
  ],
  "127.0.0.1:9090": [
    "*.a.com",
    "*.b.com",
    "*.cn"
  ]
}
```
The key is a proxy host and port, and the value is a list of domains should be proxied there.  
You can use a wildcards, as in above example.
Then, depending on the interpretation you need to use.

### PHP

Just bring a `pac.php` file together with `rules.json` in some Apache or the Nginx webserver directory.  
Set your device PAC URL to the corresponding one (e.g. `http://<YOUR_HOST>/some/path/pac.php`).  
Now every domains, you've set at `rules.json`, traffic will be going through the corresponding proxy you've specified there.


### Python

First, install the dependencies:
```bash
sh python/setup.sh
```
Then run a webserver with
```
python python/pac.py
```
Set your device PAC URL to the following: `http://<YOUR_HOST>:3128/`).  
Now every domains, you've set at `rules.json`, traffic will be going through the corresponding proxy you've specified there.
