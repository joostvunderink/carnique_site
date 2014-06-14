function quote_vote(e, direction) {
    quote_id = e.target.value;
    console.log("Voting " + direction + "; quote id = " + quote_id);
    $.post("/quotes/vote/", {
        "quote_id": quote_id,
        "direction": direction,
    })
    .done(function(data) {
        if (data.success) {
            console.log("Gestemd!");
            quote_id = data.quote_id;
            $("span#quote_score_"+quote_id).html(data.new_score);
            $("span#quote_vote_text_" + quote_id).html("Dank je voor je stem!");;
        }
        else {
            alert("Stemmen mislukt; graag contact opnemen met Garion: " + data.error)
        }
    });
};

$(document).ready(function() {
    $("button.quote_vote_up").click(function(e) {
        quote_vote(e, 'up');
    });
    $("button.quote_vote_down").click(function(e) {
        quote_vote(e, 'down');
    });
});
