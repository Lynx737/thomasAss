function deleteTask(taskid){
    fetch('/delete-task',{
        method: 'POST',
        body : JSON.stringify({ taskid:taskid})
    }).then ((_res)=>{
        window.location.href = "/";
    });
}



  