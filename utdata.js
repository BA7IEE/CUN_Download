function get_time() {
    var x;
    x = Math.round((new Date()).getTime());
    return x;
}
function get_useragent() {
    var agent;
    agent = navigator.userAgent;
    return agent;
}
function D(Z, K) {
    var U = [];
    var X = {};
    var Y = K % 100;
    for (var W = 0,
    V = Z.length; W < V; W++) {
        var a = Z.charCodeAt(W) ^ Y;
        U.push(a);
        if (!X[a]) {
            X[a] = []
        }
        X[a].push(W)
    }
    return U + ',' + K + '0';
}
function getutdata(w, h) {
    var T = (new Date()).getTime();
    var N = 100000;
    var S = Math.floor(Math.random() * N + N);
    var E = Math.floor(Math.random() * 100 + 700) + "," + Math.floor(Math.random() * 100 + 600);
    var G = "4,4,4,4,4,4,4,4,4,4";
    var U = [E, G, S, [w, h].join(",")].join("");
    var I = D(U, T);
    return I;
}


function getutdata2() {
    var T = (new Date()).getTime();
    var N = 20000;
    var S = Math.floor(Math.random() * N + N);
    var E = Math.floor(Math.random() * 100 + 700) + "," + Math.floor(Math.random() * 100 + 600);
    var Z = Math.floor(Math.random() * 10 + 1);
    var G = "3,";
    for (var W = 0; W < Z; W++) {
        if (W != Z - 1) {
            G += Math.floor(Math.random() * 4 + 1) + ",";
        } else {
            G += Math.floor(Math.random() * 4 + 1);
        }
    }
    var U = [E, G, S, [screen.width, screen.height].join(",")].join("");
    var I = D(U, T);
    return I;
}
