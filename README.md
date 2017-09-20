# dp
### Build Status
[![Build Status](https://www.travis-ci.org/millerbinbin/dp.svg?branch=master)](https://www.travis-ci.org/millerbinbin/dp)

Running on Host
 - Enter the "main" folder and execute "python web.py"

Running on Docker
```
docker build -t dp-img ./
docker run --name dp-express -p 18080:8080 dp-img -d
```
