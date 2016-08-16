Object.size = function(obj) {
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) size++;
    }
    return size;
};

function getRandomInt(minimum, maximum) {
    min = typeof minimum !== 'undefined' ? minimum : 0;
    max = typeof maximum !== 'undefined' ? maximum : 100;
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function diffJSON(o1, o2) {
    var k, kDiff,
        diff = {};
    for (k in o1) {
        if (!o1.hasOwnProperty(k)) {
        } else if (typeof o1[k] != 'object' || typeof o2[k] != 'object') {
            if (!(k in o2) || o1[k] !== o2[k]) {
                diff[k] = o2[k];
            }
        } else if (kDiff = difference(o1[k], o2[k])) {
            diff[k] = kDiff;
        }
    }
    for (k in o2) {
        if (o2.hasOwnProperty(k) && !(k in o1)) {
            diff[k] = o2[k];
        }
    }
    for (k in diff) {
        if (diff.hasOwnProperty(k)) {
			diff.id = o1._id;
            return diff;
        }
    }
    return false;
}

function getJSON(url, cb) {
    var client = new XMLHttpRequest();
    client.onload = function() {
        if(this.status == 200)
            cb(JSON.parse(this.response));
        else {
            //console.log('error');
        }
    }
    client.open("GET", url);
    client.send();
}
