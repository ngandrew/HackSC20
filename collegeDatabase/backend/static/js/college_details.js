$(document).ready(() => {
    const urlParams = new URLSearchParams(window.location.search);
    fetch(`api/college_details?id=${urlParams.get('id')}&income=${urlParams.get('income')}`)
    .then(res => res.json())
    .then(({
        name,
        city,
        state,
        publicPrivate,
        sat_scores,
        act_scores,
        expectedCost,
        difficulty,
        inState,
        outOfState,
        roomAndBoard,
        essays,
        appFee,
        isUc,
        calculatorLink,
        deadline,
        athletics,
        grad4,
        grad5,
        grad6,
        classSize,
        website
    }) => {
        let satString = "";
        if (sat_scores) {
            if (sat_scores[0] && sat_scores[2]) {
                satString = `${sat_scores[0]}-${sat_scores[2]}`;
            } else {
                satString = sat_scores[1];
            }
        }

        let actString = "";
        if (act_scores) {
            if (act_scores[0] && act_scores[2]) {
                actString = `${act_scores[0]}-${act_scores[2]}`;
            } else {
                actString = act_scores[1];
            }
        }

        $('.bradcam_text a h3').html(name);
        $('.bradcam_text a').attr('href', website);
        $('.links_locat').empty()
        .append($(`<div class="location">
                        <p> <i class="fa fa-map-marker"></i> ${city}, ${state}</p>
                    </div>`))
        .append($(`<div class="location">
                        <p> <i class="fa fa-building"></i>${publicPrivate}</p>
                    </div>`))
        .append($(`<div class="location">
                        <p> <i class="fa fa-edit"></i>SAT: ${satString}</p>
                    </div>`))
        .append($(`<div class="location">
                    <p> <i class="fa fa-edit"></i>ACT: ${actString}</p>
                </div>`));

        $('.descript_wrap ul.financial').empty()
        .append($(`<li>Estimated in-state Tuition: <span>$${Number(inState).toLocaleString()}</span></li>`))
        .append($(`<li>Estimated out-of-state Tuition: <span>$${Number(outOfState).toLocaleString()}</span></li>`))
        .append($(`<li>Estimated Room and Board:  <span>$${Number(roomAndBoard).toLocaleString()}</span></li>`))
        .append($(`<li>Personalized Cost Estimate: <span>$${Number(expectedCost).toLocaleString()}</span></li>`))
        .append($(`<a href="${calculatorLink}" class="boxed-btn3" target="blank">Calculate your Tuition</a>`));

        $('.descript_wrap ul.other').empty()
        .append($(`<li>Undergraduate class size: <span>${classSize}</span></li>`))
        .append($(`<li>College Sports: <span>${athletics}</span></li>`))
        .append($(`<li>Graduation within 4 years: <span>${grad4}%</span></li>`))
        .append($(`<li>Graduation within 5 years: <span>${grad5}%</span></li>`))
        .append($(`<li>Graduation within 6 years: <span>${grad6}%</span></li>`));

        $('.job_sumary .job_content ul').empty()
        .append($(`<li>Regular Due Date: <span>${deadline}</span></li>`))
        .append($(`<li>Additional essays: <span>${essays ? 'Yes' : 'No'}</span></li>`))
        .append($(`<li>Application Fee: <span>${appFee}</span></li>`))
        .append($(`<li>Competitiveness: <span>${difficulty}</span></li>`))
        .append($(isUc ?
                    '' :
                    `<li>Accepts <a href="https://apply.commonapp.org/login" style="text-decoration: underline;">Common Application</a></li>`));
        document.title = `College Details – ${name}`;

    });
});
