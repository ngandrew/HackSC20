$(document).ready(() => {
    $('#searchCollegeButton').click(() => {
        let income = parseInt($('#estIncome').val());
        let satScore = parseInt($('#SAT').val());
        let actScore = parseInt($('#ACT').val());
        let publicPrivate = $('#publicPrivate option:selected').val();

        let data = {
            income,
            satScore,
            actScore,
            publicPrivate,
        };

        fetch(`api/colleges?data=${JSON.stringify(data)}`)
        .then(res => res.json())
        .then(res => {
            $('.job_lists .row').empty();
            res.forEach(({
                id,
                name,
                city,
                state,
                publicPrivate,
                sat25,
                sat75,
                act25,
                act75,
                expectedCost,
                difficulty,
                calculatorLink,
                deadline,
                website,
            }) => {
                const newContent = $(`
                <div class="col-lg-12 col-md-12">
                    <div class="single_jobs white-bg d-flex justify-content-between">
                        <div class="jobs_left d-flex align-items-center">
                            <div class="jobs_conetent" style="width:100%;">
                                <a href="job_details.html?id=${id}"><h4>${name}</h4></a>
                                <div class="links_locat d-flex align-items-center">
                                    <div class="location">
                                        <p> <i class="fa fa-map-marker"></i> ${city}, ${state}</p>
                                    </div>
                                    <div class="location">
                                        <p> <i class="fa fa-building"></i>${publicPrivate}</p>
                                    </div>
                                    <div class="location">
                                        <p> <i class="fa fa-edit"></i>SAT: ${sat25}-${sat75}</p>
                                    </div>
                                    <div class="location">
                                        <p> <i class="fa fa-edit"></i>ACT: ${act25}-${act75}</p>
                                    </div>
                                    <div class="location">
                                        <p title="Includes room and board & est. financial aid"> <i class="fa fa-credit-card"></i>Expected Cost: $${Number(expectedCost).toLocaleString()}</p>
                                    </div>
                                    <div class="location">
                                        <p> <i class="fa fa-exclamation-triangle"></i>${difficulty}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="jobs_right">
                            <div class="apply_now pull-right">
                                <a href="${calculatorLink}" class="boxed-btn3" target="blank"><i class="fa fa-calculator"></i></a>
                            </div>
                            <div class="date pull-right">
                                <p>Deadline: ${deadline}</p>
                            </div>
                        </div>
                        <div style="width:100%"></div>
                        <a href="${website}" target="_blank">Go to Website</a>
                    </div>
                </div>`);
                $('.job_lists .row').append(newContent);
            });
        });
    });
});
