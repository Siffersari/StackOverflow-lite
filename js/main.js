function deleter(){
    var purges = confirm('This change is irreversible. Do you want to proceed ?');
    
    if (purges) {
        alert('This question has been deleted.');
        window.location.replace("post.html");
    }
}