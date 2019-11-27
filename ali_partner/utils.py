import trafaret as T

primitive_ip_regexp = r'^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'

TRAFARET_CONF = T.Dict({
    T.Key('host'): T.Regexp(primitive_ip_regexp),
    T.Key('port'): T.Int(),
    T.Key('debug'): T.Dict({
        T.Key('status', default=False): T.Bool(),
        T.Key('console', default=False): T.Bool(),
    })
})
