var express = require('express');
var router = express.Router();
var request = require('request');
var fs = require('fs');
var parse = require('csv-parse');


/* GET home page. */
router.get('/', function(req, res, next) {
	res.render('index', {'title':'Mindwave'});
});

router.get('/stations', function(req, res, next) {
	fs.createReadStream('stations.csv').pipe(parse({delimiter: ','}, function(err, data){
		res.render('stations', {'title':'BDI', 'locs': data});
	}));
});

module.exports = router;
