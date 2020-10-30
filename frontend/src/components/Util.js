export function fetchRequest(methodType, url, func = console.log, body = null) {
    if (methodType === 'GET') {
        fetch(url)
        .then(response => response.json())
        .then(data => {func(data);
        }).catch(err => console.error('YOU GOT AN ERROR: ', err))
    }
    else if (methodType === 'POST') {
        // debugger;
        fetch(url, {
            method: 'POST',
            body: JSON.stringify(body),
            headers: {
                "content-type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {func(data);
        }).catch(err => console.error('YOU GOT AN ERROR: ', err))
    } else if (methodType === 'DELETE') {
        fetch(url, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {func(data);
        }).catch(err => console.error('YOU GOT AN ERROR: ', err))
    } else if (methodType === 'PUT') {
        fetch(url, {
            method: 'PUT'
        })
        .then(response => response.json())
        .then(data => {func(data);
        }).catch(err => console.error('YOU GOT AN ERROR: ', err))
    }
}