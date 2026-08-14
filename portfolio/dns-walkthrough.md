# Plain-Language DNS Walkthrough

My portfolio is currently published at `bilgenurpala.netlify.app`. Netlify gives this site a public HTTPS address and serves the built HTML, CSS, JavaScript, images, and CV when a visitor requests them. FlyRank will provide its subdomain after the capstone is approved, so I have not created or claimed a FlyRank DNS record yet.

A CNAME record is a DNS instruction that says one hostname is an alias of another hostname. It does not contain the website files and it is not a redirect shown in the browser. The record stores a target hostname. For example, if FlyRank later gives me a hostname such as `bilgenur.flyrank.ai`, its DNS configuration could use a CNAME whose value points to the hostname Netlify tells me to use. I would copy Netlify's exact target value rather than guess it.

When someone enters the FlyRank address, the browser first asks a DNS resolver where that name should go. The resolver may already have a recent answer in its cache. If it does not, it follows the DNS hierarchy until it reaches the authoritative nameserver for the domain. That nameserver returns the CNAME record. The resolver then looks up the CNAME target and returns the destination information to the browser. The browser connects to Netlify, checks the HTTPS certificate for the requested address, and asks for the page. Netlify matches the hostname to my deployed site and sends the response.

DNS changes are not always visible everywhere at the same moment because resolvers cache answers for the record's TTL, or time to live. This delay is commonly called propagation. After adding the real record, I would wait for Netlify to recognize it and issue the HTTPS certificate, then test the final address in a private window and on a second device. I would verify that all four routes work, that the certificate is valid, and that the address stays on the intended domain while navigating.

Until FlyRank provisions the subdomain, the valid public delivery address is `https://bilgenurpala.netlify.app/`.
