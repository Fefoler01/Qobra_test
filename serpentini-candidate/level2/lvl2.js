
// import json file
import jsonData from './data/input.json' assert { type: 'json' };

// sum of deals by user
var user = {};
for (var i_deal = 0; i_deal < jsonData.deals.length; i_deal++) { // loop through deals
    if (jsonData.deals[i_deal].user in user) { // if user already exists
        user[jsonData.deals[i_deal].user] += jsonData.deals[i_deal].amount;
    } else { // first deal for this user
        user[jsonData.deals[i_deal].user] = jsonData.deals[i_deal].amount;
    }
}
console.log(user);

// comparaison between deals and objectives to calculate commissions
var result = {"commissions":[]};
for (var i_user in user) {
    var objective = 100*user[i_user] / jsonData.users[i_user-1].objective; // objective reach by user in %

    result.commissions[i_user-1] = {};
    result.commissions[i_user-1].user_id = i_user;
    result.commissions[i_user-1].commission = 0;
    if (objective > 100) { // for commission part over 100%
        result.commissions[i_user-1].commission += (user[i_user]-jsonData.users[i_user-1].objective)*0.15; // total - objective
    }
    if (objective > 50) { // for commission part over 50%
        result.commissions[i_user-1].commission += (user[i_user]-result.commissions[i_user-1].commission-jsonData.users[i_user-1].objective*0.5)*0.1; // total - commission>100% - demi-objective
    }
    // for commission part under 50%
    result.commissions[i_user-1].commission += (user[i_user]-result.commissions[i_user-1].commission)*0.05; // total - (commission>100% + commission>50%)
        
}
console.log(result);


// write result in json file
const fs = require('fs');
fs.writeFile('./data/output.json', JSON.stringify(result), (err) => {
    if (err) throw err;
    console.log('Complete!');
});
