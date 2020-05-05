var Ui = {
    // initialize page view
    initializeView: function() {
        var svg = d3.select('svg');
        CTRL.get_content_size(svg.attr("width"), svg.attr("height"));
    },

    // initialize tooltips
    initializeTooltips: function() {
        d3.select("svg")
            .append("g")
                .attr("id", "tooltip-box")
            .append("rect")
                .attr("x", 0)
                .attr("y", 0)
                .attr("width", 20)
                .attr("height", 10)
                .attr("fill", "#FF0000AA")
    },

    // search devices
    findDevices: function() {
        // var descs = Array.prototype.slice.call(document.querySelectorAll("desc"));
        var descs = d3.selectAll("desc").nodes();
        descs.forEach(function(desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if(result) {
                var devname = result[1], parent = desc.parentNode;
                console.log("Found device: " + devname +
                            " (" + parent.getAttribute("id") + ")");
                CTRL.registerDevice(devname);
                //parent.classList.add('tooltip');
                if (!parent.onclick)
                    parent.onclick = function(evt) {
                        CTRL.select(devname);
                };
                if (!parent.ondblclick)
                    parent.ondblclick = function(evt) {
                        CTRL.dblSelect(devname);
                };
                if (!parent.onmouseover)
                    parent.onmouseover = function(evt) {
                        CTRL.mouseOver(devname);
                };

                // check
                var elems = Ui.getElementsByDeviceName(devname);
                if (elems.length > 1) {
                    console.log(devname + " has more than one elements.");
                };
            }
        });
        CTRL.loadDeviceDone();
    },

    // find anchors for annotations
    findAnnotes: function() {
        var annotes = Array.prototype.slice.call(document.querySelectorAll("desc"));
        annotes.forEach(function (annote) {
            var result = /annote=(.*)/.exec(annote.textContent);
            if (result) {
                var conf = result[1].split(",");
                var devname = conf[0];
                var fname = conf[1];
                if (conf[2]) {
                    handle = conf[2];
                } else {
                    handle = 'readback';
                }
                if (conf[3]) {
                    nprec = Number(conf[3]);
                } else {
                    nprec = 4;
                }
                console.log("Found annote anchor: " + devname + " " + fname + " " + handle + " " + nprec);
                CTRL.registerAnnoteAnchor(devname, fname, handle, nprec);
            }
        });
    },

    getElementsByAnnoteTuple: function (devname, fname, handle, nprec) {
        var els = [];
        var annotes = Array.prototype.slice.call(document.querySelectorAll("desc"));
        annotes.forEach(function (annote) {
            var result = /annote=(.*)/.exec(annote.textContent);
            if (result) {
                var conf = result[1].split(",");
                var devname1 = conf[0];
                var fname1 = conf[1];
                if (conf[2]) {
                    handle1 = conf[2];
                } else {
                    handle1 = 'readback';
                }
                if (conf[3]) {
                    nprec1 = Number(conf[3]);
                } else {
                    nprec1 = 4;
                }
                if (devname1 == devname && fname1 == fname && handle1 == handle && nprec1 == nprec) {
                    els.push(annote.parentNode);
                }
            }
        });
        return els;
    },

    getElementsByDeviceName: function(devname) {
        var els = [];
        var descs = d3.selectAll("desc").nodes()
        descs.forEach(function(desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if (result && result[1] == devname) {
                els.push(desc.parentNode);
            }
        });
        return els;
    },

    findParentDevice: function (el) {
        while (el) {
            var devname = Stuff.getDeviceName(el);
            if (devname)
                return devname;
            el = el.parentNode;
        }
        return null;
    },

    getDeviceName: function (el) {
        var desc = el.querySelector("desc");
        if (desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if (result)
                return result[1];
        }
        return null;
    },

    toggle: function (evt) {
        evt.stopPropagation();
        var target = evt.currentTarget;  // makes sure we get <g> element if the onclick is on it
        var devname = Stuff.findParentDevice(target);
        console.log("toggle", devname);
        if (devname)
            TANGO.toggle(devname);
        else
            console.log("no device for element " + target.getAttribute("id"));
        return false;
    },

    // create a rect for top notation
    getTopRectFromElement: function (elm) {
        var bb = elm.getBBox();
        var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("width", 10);
        rect.setAttribute("height", 5);
        rect.setAttribute("x", bb.x + bb.width * 0.5 - 5.0);
        rect.setAttribute("y", bb.y + 5 + 1);
        rect.setAttribute("style",
            "fill:#EEEEEC;stroke:orange;fill-opacity:0.5;stroke-opacity:0.7;stroke-width:0.5;");
        return rect;
    },

    getBBoxAsRectElement: function (elm){
        var bb = elm.getBBox();
        var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        console.log("bbrect " + bb.width + ", " + bb.height);
        var padding = 0.2 * Math.min(bb.width, bb.height);
        rect.setAttribute("width", bb.width + 1.0 * padding);
        rect.setAttribute("height", bb.height + 1.0 * padding);
        rect.setAttribute("x", bb.x - padding);
        rect.setAttribute("y", bb.y - padding);
        rect.setAttribute("rx", 1.0 * padding);
        rect.setAttribute("ry", 1.0 * padding);
        rect.setAttribute("class", "select");
        return rect;
    },

    removeElementsOfClass: function(cls) {
        d3.selectAll("." + cls).classed(cls, false);
    },

    hover: function(devname) {
        console.log("Hover: " + devname);
        Ui.removeElementsOfClass("hover");
        var elements = Ui.getElementsByDeviceName(devname);
        elements.forEach(function(el) {
            d3.select("#" + el.id).classed("hover", true);
        });
    },

    // place top rect
    addTopRect: function (devname) {
        var elements = Ui.getElementsByDeviceName(devname);
        elements.forEach(function (el) {
            console.log("Add top rect for " + devname);
            var rect = Ui.getTopRectFromElement(el);
            el.parentNode.insertBefore(rect, el);
        });
    },

    // select device
    select: function(devname) {
        var cls = "select";
        var element = Ui.getElementsByDeviceName(devname)[0];
        var o = d3.select("#" + element.id);
        if (o.classed(cls)) {
            o.classed(cls, false);
        } else {
            Ui.removeElementsOfClass(cls);
            o.classed(cls, true);
        }
        CTRL.updateSelection(devname, o.classed(cls));
    },

    setStatus: function (devname, status) {
        console.log("setStatus " + devname + " " + status);
        var els = Ui.getElementsByDeviceName(devname);
        els.forEach(function (el) {
            console.log("id: " + el.getAttribute("id"));
            el.setAttribute("class", "status-" + status);
            console.log(el.getAttribute("class"));
        });
        // set status
    },

    // put value to defined anchor
    updateData: function (value, devname, fname, handle, nprec) {
        console.log(
            "updateData " + value + " for " + devname + " [" + fname + "] " + "of handle: " + handle);
        var elems = Ui.getElementsByAnnoteTuple(devname, fname, handle, nprec);
        var tspan_list = elems[0].getElementsByTagName('tspan');
        if (tspan_list.length >= 1) {
            t = tspan_list[0];
            t.textContent = fname + "|" + value.toFixed(nprec);
        };
    },
};
