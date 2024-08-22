function FindProxyForURL(url, host) {
    if (shExpMatch(host, "oneroster.lvusd.org") || 
        shExpMatch(host, "api.5starstudents.com")) {
      return "PROXY 192.168.68.100:8080";
    }
    return "DIRECT";
  }
  