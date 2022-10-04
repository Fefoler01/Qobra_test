

// import json file
import jsonData from './data/input.json' assert { type: 'json' };

console.log(jsonData);

// sum of deals by user
var user = {};
for (var i_deal = 0; i_deal < jsonData.deals.length; i_deal++) {
    if (jsonData.deals[i_deal].user in user) {
        user[jsonData.deals[i_deal].user] += jsonData.deals[i_deal].amount;
    } else {
        user[jsonData.deals[i_deal].user] = jsonData.deals[i_deal].amount;
    }
}
console.log(user);

// comparaison between deals and objectives
var result = {"commissions":[]};
for (var i_user in user) {
    console.log(user[i_user]);
    var objective = 100*user[i_user] / jsonData.users[i_user-1].objective;

    result.commissions[i_user-1] = {};
    result.commissions[i_user-1].user_id = i_user;
    result.commissions[i_user-1].commission = 0;
    if (objective > 100) {
        result.commissions[i_user-1].commission += (user[i_user]-jsonData.users[i_user-1].objective)*0.15;
    }
    if (objective > 50) {
        result.commissions[i_user-1].commission += (user[i_user]-result.commissions[i_user-1].commission-jsonData.users[i_user-1].objective*0.5)*0.1;
    }
    result.commissions[i_user-1].commission += (user[i_user]-result.commissions[i_user-1].commission)*0.05;
        
}
console.log(result);

/* write result in json file */



/* write result in json file
const fs = require('fs');
fs.writeFile('./data/output.json', JSON.stringify(result), (err) => {
    if (err) throw err;
    console.log('Complete!');
});*/
//export default JSON.stringify(result);

console.log('End');