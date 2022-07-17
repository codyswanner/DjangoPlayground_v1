document.forms.new_book.addEventListener ('click', e => {
    if (e.target.name == "add_author_btn" && e.target.form.author2Fields.disabled == true) {
        console.log(e)
        e.target.form.author2Fields.disabled = false;
    } else if (e.target.name == "remove_author_btn" && e.target.form.author3Fields.disabled == false) {
        console.log(e)
        e.target.form.author3Fields.disabled = true;
    } else if (e.target.name == "add_author_btn" && e.target.form.author3Fields.disabled == true) {
        console.log(e)
        e.target.form.author3Fields.disabled = false;
    } else if (e.target.name == "remove_author_btn" && e.target.form.author2Fields.disabled == false) {
        console.log(e)
        e.target.form.author2Fields.disabled = true;
    }
})


document.forms.new_book.addEventListener ('change', e => {
    if (e.target.value == 'True') {
        e.target.form.seriesField.disabled = false;
    } else {
        e.target.form.seriesField.disabled = true;
    }
})