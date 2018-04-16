/**
 * Mostly stolen from the D3 examples page.
 *
 * http://mbostock.github.io/d3/talk/20111018/tree.html
 */

"use strict";

var dx = 20,
    dy = 0,
    w = 290,
    h = 830,
    i = 0,
    parents = [],
    selectedNode = null,
    root;

var tree = d3.layout.tree()
    .size([h, w]);

var diagonal = d3.svg.diagonal()
    .projection(function(d) { return [d.y, d.x]; });

d3.select("#ancestry_container")
    .style("width", w + "px")
    .style("height", h + "px");

var vis = d3.select("#ancestry_chart")
    .attr("width", w)
    .attr("height", h)
    .append("svg:g")
    .attr("transform", "translate(" + 90 + "," + 0 + ")");

d3.json("json/ancestry.json", function(json) {
    window.jsondata = json;

    addParents(json, null);

    root = json;
    root.x0 = h / 2;
    root.y0 = 0;

    function toggleAll(d) {
        if (d.children) {
            d.children.forEach(toggleAll);
            toggle(d);
        }
    }

    root.children.forEach(toggleAll);

    update(root);

    initTypeahead(json);
});

function update(source) {
    var duration = d3.event && d3.event.altKey ? 5000 : 500;

    // Compute the new tree layout.
    var nodes = tree.nodes(root).reverse();

    // Normalize for fixed-depth.
    nodes.forEach(function(d) { d.y = d.depth * 180; });

    // Update the nodes...
    var node = vis.selectAll("g.node")
        .data(nodes, function(d) { return d.id || (d.id = ++i); });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("svg:g")
        .attr("class", "node")
        .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
        .on("click", function(d) {
            selectedNode = null;
            if (d === root || d._children) {
                makeRoot(d);
                update(d);
            }
        });

    nodeEnter.append("svg:circle")
        .attr("r", 1e-6)
        .style("fill", fillNode);

    // name
    nodeEnter.append("svg:text")
        .attr("x", 5)
        .attr("dy", "-1em")
        .attr("text-anchor", "end")
        .text(function(d) { return d.name; })
        .style("fill-opacity", 1e-6);

    // number of descendants
    nodeEnter.append("svg:text")
        .attr("class", "descendants")
        .attr("x", -8)
        .attr("dy", "1.5em")
        .attr("text-anchor", "start")
        .text(function(d) {
            return d.children || d._children
                ? '(' + (subtreeSize(d) - 1) + ')'
                : "";
        })
        .style("fill-opacity", 1e-6);

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

    nodeUpdate.select("circle")
        .attr("r", 6)
        .style("fill", fillNode);

    nodeUpdate.select("text")
        .attr("x", function(d) { return d === root ? 40 : 5; })
        .style("fill-opacity", 1);

    nodeUpdate.select("text.descendants")
        .style("fill-opacity", function(d) { return d === root ? 0 : 0.25; });

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
        .remove();

    nodeExit.select("circle")
        .attr("r", 1e-6);

    nodeExit.select("text")
        .style("fill-opacity", 1e-6);

    // Update the links…
    var link = vis.selectAll("path.link")
        .data(tree.links(nodes), function(d) { return d.target.id; });

    // Enter any new links at the parent's previous position.
    link.enter().insert("svg:path", "g")
        .attr("class", "link")
        .attr("d", function(d) {
            var o = {x: source.x0, y: source.y0};
            return diagonal({source: o, target: o});
        })
        .transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function(d) {
            var o = {x: source.x, y: source.y};
            return diagonal({source: o, target: o});
        })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function(d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

function fillNode(d) {
    if (d === selectedNode) {
        return "rgba(255, 0, 0, 0.5)";
    }
    return (d._children || d.children) ? "rgb(0, 128, 0)" : "lightsteelblue";
}

// Toggle children.
function toggle(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
}

function makeRoot(d) {
    if (d !== root) {
        parents.push(root);
        root = d;
    } else if (parents.length) {
        toggle(root);
        root = parents.pop();
    }

    if (root._children) {
        toggle(root);
    }
}

function moveUp() {
    if (root.children) {
        toggle(root);
    }

    if (parents.length) {
        root = parents.pop()
    }
}

/**
 * Add parent backpointers to each node in the tree.
 */
function addParents(json, parent) {
    json.parent = parent;

    if (!json.children) {
        return;
    }

    for (var i = 0; i < json.children.length; ++i) {
        addParents(json.children[i], json);
    }
}

function dfs(json, targetName) {

    function dfsHelper(json) {
        if (json.name === targetName) {
            return [json.name];
        }

        var children = json.children || json._children;
        if (children) {
            for (var i = 0; i < children.length; ++i) {
                var result = dfsHelper(children[i]);
                if (result) {
                    return [json.name].concat(result);
                }
            }
        }

        return null;
    }

    var result = dfsHelper(json);
    return result;
}

function collectNames(json) {
    var childrenNames = [];
    var children = json.children || json._children;
    if (children) {
        childrenNames = children.map(collectNames);
    }

    var names = [json.name];
    for (var i = 0; i < childrenNames.length; ++i) {
        names = names.concat(childrenNames[i]);
    }

    return names;
}

function initTypeahead(json) {
    var player_names = collectNames(json);
    window.players = player_names;

    $('input.typeahead').typeahead({
        name: 'players',
        local: player_names,
    }).on('typeahead:selected', function(e, datum, id) {
        switchTo(datum.value);
    }).on('typeahead:autocompleted', function(e, datum, id) {
        switchTo(datum.value);
    }).on('keypress', function(e) {
        // Enter key
        if (e.which === 13 &&
            $.inArray($('.typeahead').val(), player_names) !== -1) {

            switchTo($('.typeahead').val());

            // Close suggestions
            $('.typeahead').trigger('blur');
        }
    });
}

/**
 * Return to the root, then descend the tree until we reach the desired player.
 */
function switchTo(zombieName) {
    while (parents.length) {
        moveUp();
    }

    // Make the selected element's _parent_ into the root
    var path = dfs(root, zombieName);
    for (var i = 1; i < path.length - 1; ++i) {
        var children = root.children || root._children;
        for (var j = 0; j < children.length; ++j) {
            if (children[j].name === path[i]) {
                makeRoot(children[j]);
            }
        }
    }

    // Highlight the chosen node
    for (var i = 0; i < root.children.length; ++i) {
        if (root.children[i].name === zombieName) {
            if (root.children[i].children || root.children[i]._children) {
                // If the node has children, make it the root.
                makeRoot(root.children[i]);
            } else {
                // If the node has no children, show its parent and highlight it
                selectedNode = root.children[i];
            }
        }
    }

    if (selectedNode && selectedNode.name !== zombieName) {
        selectedNode = null;
    }

    update(root);
    return root;
}

function subtreeSize(node) {
    var children = node.children || node._children;

    if (!children) {
        return 1;
    }

    var count = 1;
    for (var i = 0; i < children.length; ++i) {
        count += subtreeSize(children[i]);
    }

    return count;
}

(function() {
    $('.scriptonly').show();
    $('.noscript').remove();
})();
