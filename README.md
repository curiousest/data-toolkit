# data-toolkit

A jupyter notebook setup.

## Run

```sh
docker-compose up -d
docker-compose logs --tail 20
```

* You will see the token necessary to connect (if you're using pycharm, settings->jupyter)
* Point your browser to localhost:8888 to log onto the jupyter notebook

### AWS EC2 Notebook Server

You can spin up an AWS EC2 instance to run the notebook server and any other docker containers you need. See [the fabfile](https://github.com/curiousest/data-toolkit/blob/master/fabfile.py#L10).
