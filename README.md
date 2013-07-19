Description
===========

rb-on-gpudeath aims to check the GPU health through cgminers RPC api.

This is a Linux port of [waffle_stompers](http://www.reddit.com/u/waffle_stomper) Script from [here](http://www.reddit.com/r/litecoinmining/comments/1ilplj/automatic_reboot_script_for_when_a_card_is/).

The initial GIST [here](https://gist.github.com/wvvw/113b5f48933a8220e7b7)


Using
=====

Start cgminer with --api-allow 127/8 --api-port 4028 --api-listen

OR

pur this in your config:

	"api-listen" : true,
	"api-allow" : "W:127.0.0.1",
	"api-port" : "4028",
