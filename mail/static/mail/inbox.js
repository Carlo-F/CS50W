document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  const form = document.querySelector('#compose-form');
    
  form.addEventListener('submit', (event) => send_email(form, event));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mailbox-content').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#mailbox-title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    result.forEach(email => {
      const box = document.createElement('div');
      box.classList.add('card', 'mb-2', 'p-4');

      if (email.read) {
        box.classList.add('bg-light');
      }
      
      const sender = document.createElement('h5');
      sender.innerHTML = email.sender
      sender.classList.add('card-title','font-weight-bold');

      box.append(sender);

      const timestamp = document.createElement('h6');
      timestamp.innerHTML = email.timestamp
      timestamp.classList.add('card-subtitle','mb-2','text-body-secondary');

      box.append(timestamp);

      const body = document.createElement('p');
      body.innerHTML = email.body;
      body.classList.add('card-text','pl-2');

      box.append(body);

      document.querySelector('#mailbox-content').append(box);
    })
  });

}

function send_email(form, event) {
  event.preventDefault()

  const formData = new FormData(form)

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: formData.get('compose-recipients'),
        subject: formData.get('compose-subject'),
        body: formData.get('compose-body')
    })
  })
  .then(response => response.json())
  .then(result => {
    //load sent mailbox
    load_mailbox('sent');
  });
}