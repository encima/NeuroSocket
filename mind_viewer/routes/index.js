var express = require('express');
var router = express.Router();
var request = require('request');
var fs = require('fs');
var parse = require('csv-parse');


/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('index', {'title':'Mindwave'});
});

module.exports = router;
