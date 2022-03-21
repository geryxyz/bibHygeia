/**
 * @type {Report}
 */
var report;

const templates = {
    entry_failure: $('#template-entry-failure').contents(),
    fileline_failure: $('#template-fileline-failure').contents(),
    hint: $('#template-hint').contents()
}

const entry_failures_html = $('#entry-failures');
const fileline_failures_html = $('#fileline-failures');

/**
 * @param {EntryFailure} failure
 */
function render_entry_failure(failure) {
    const entry_failure_html = templates.entry_failure.clone();
    const entry = report.entries[failure.entry_key];
    
    entry_failure_html.find('.failure-message').text(failure.message);

    entry_failure_html.find('.entry-key').text(entry.key);
    entry_failure_html.find('.entry-type').text(entry.type);
    entry_failure_html.find('.entry-file-path').text(entry.file_path);
    entry_failure_html.find('.entry-line-number').text(entry.line_number);

    failure.hints.map(function (hint) {
        const hint_html = templates.hint.clone();

        hint_html.find('.hint-title').text(hint.title);
        hint_html.find('.hint-recommendation').text(hint.recommendation);
        hint_html.find('.hint-reason').text(hint.reason);

        entry_failure_html.find('.hints').append(hint_html);
    });

    entry_failures_html.append(entry_failure_html);
}

/**
 * @param {FileLineFailure} failure
 */
function render_fileline_failure(failure) {
    const fileline_failure_html = templates.fileline_failure.clone();

    fileline_failure_html.find('.failure-message').text(failure.message);

    fileline_failure_html.find('.entry-file-path').text(failure.file_path);
    fileline_failure_html.find('.entry-line-number').text(failure.line_number);

    fileline_failures_html.append(fileline_failure_html);
}

var start_time = new Date(0);
start_time.setUTCSeconds(report.start_time);

var end_time = new Date(0);
end_time.setUTCSeconds(report.end_time);

$('#start-time').text(start_time.toLocaleString());
$('#end-time').text(end_time.toLocaleString());
$('#failure-count').text(report.failures.length);

report.failures.map(function (failure, index) {
    if (failure.type === "entry") {
        render_entry_failure(failure);
    }
    else if(failure.type === "fileline") {
        render_fileline_failure(failure);
    }
});