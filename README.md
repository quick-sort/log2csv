Log2csv
=======
A tool to parse unstructured log files into structured csv, using a grok-like pattern.

```
log2csv [-p custom_pattern.grok|custom_pattern_dir]  [-o output.csv] -e '%{NUMBER:size} (?P<custom_name>regexpression) (?:content to ignore but match) %{IP: client} %{UserAgent: agent} %{URL: request_url}' nginx.log
```

## Expression

```
%{PATTERN_NAME1: csv_field_name}
%{PATTERN_NAME2}
```

## Grok File

```
PATTERN_NAME1 regexpression
PATTERN_NAME2 %{SUB_PATTERN: field_name}
# Comment
```

## Example

sample.log
```
77.179.66.156 - - [25/Oct/2016:14:49:33 +0200] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
77.179.66.156 - - [25/Oct/2016:14:49:34 +0200] "GET /favicon.ico HTTP/1.1" 404 571 "http://localhost:8080/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
77.179.66.156 - - [25/Oct/2016:14:50:44 +0200] "GET /adsasd HTTP/1.1" 404 571 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"
77.179.66.156 - - [07/Dec/2016:10:34:43 +0100] "GET / HTTP/1.1" 200 612 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
77.179.66.156 - - [07/Dec/2016:10:34:43 +0100] "GET /favicon.ico HTTP/1.1" 404 571 "http://localhost:8080/" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
77.179.66.156 - - [07/Dec/2016:10:43:18 +0100] "GET /test HTTP/1.1" 404 571 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
77.179.66.156 - - [07/Dec/2016:10:43:21 +0100] "GET /test HTTP/1.1" 404 571 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
77.179.66.156 - - [07/Dec/2016:10:43:23 +0100] "GET /test1 HTTP/1.1" 404 571 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
127.0.0.1 - - [07/Dec/2016:11:04:37 +0100] "GET /test1 HTTP/1.1" 404 571 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36"
127.0.0.1 - - [07/Dec/2016:11:04:58 +0100] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"
127.0.0.1 - - [07/Dec/2016:11:04:59 +0100] "GET / HTTP/1.1" 304 0 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"
127.0.0.1 - - [07/Dec/2016:11:05:07 +0100] "GET /taga HTTP/1.1" 404 169 "-" "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:49.0) Gecko/20100101 Firefox/49.0"
```

log2csv command
```
log2csv -e '%{IP:ip} - - \[%{HTTPDATE:date}\] "%{WORD:http_method} %{URIPATH:path} HTTP/1.1" %{NUMBER:http_status} %{NUMBER:payload_bytes} "-" "%{QS:user_agent}"' sample.log
```

