document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  const form = document.querySelector('#compose-form');
    
  form.addEventListener('submit', (event) => send_email(form, event));

  // By default, load the inbox
  load_mailbox('inbox');
});

async function archive_email(email_id, archive = true) {
  
  await fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        archived: archive
      })
  })

  load_mailbox('inbox')
  
}

async function view_email(email_id, mailbox) {
  // Show email view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content').innerHTML = '';
  document.querySelector('#email-view').style.display = 'block';

  let email;

  await fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(result => {
      email = result
    })
  
  const box = document.createElement('div');
  box.classList.add('p-4');

  const sender = document.createElement('h5');
  sender.innerHTML = `<strong>From:</strong> ${email.sender}`;
  sender.classList.add('mb-2');

  box.append(sender);
      
  const recipients = document.createElement('h5');
  recipients.innerHTML = `<strong>To:</strong> ${email.recipients.join(', ')}`;
  recipients.classList.add('mb-2');

  box.append(recipients);
      
  const subject = document.createElement('h5');
  subject.innerHTML = `<strong>Subject:</strong> ${email.subject}`;
  subject.classList.add('mb-2');

  box.append(subject);

  const timestamp = document.createElement('h5');
  timestamp.innerHTML = `<strong>Timestamp:</strong> ${email.timestamp}`;
  timestamp.classList.add('mb-2');

  box.append(timestamp);
      
  const hr = document.createElement('hr');
  box.append(hr);

  const body = document.createElement('p');
  body.innerHTML = email.body;
  body.classList.add('card-text','pl-2');

  box.append(body);

  const reply_button = document.createElement('button');
  reply_button.innerHTML = 'Reply';
  reply_button.classList.add('btn', 'btn-outline-primary', 'mr-2');

  reply_button.addEventListener('click', () => compose_email(email_id));
    
  box.append(reply_button);

  if (mailbox != 'sent') {
    const button = document.createElement('button');
    button.innerHTML = email.archived ? 'Unarchive' : 'Archive';
    button.classList.add('btn', 'btn-outline-secondary');

    button.addEventListener('click', () => archive_email(email_id, !email.archived));
    
    box.append(button);
  }
  
  document.querySelector('#email-content').append(box);
  
  if (!email.read) {
    fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
        read: true
      })
    })
  }

}

async function compose_email(email_id = null) {

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  if (email_id) {

    await fetch(`/emails/${email_id}`)
      .then(response => response.json())
      .then(result => {
        document.querySelector('#compose-recipients').value = result.sender;
        document.querySelector('#compose-subject').value = result.subject.startsWith('Re: ') ? result.subject : `Re: ${result.subject}`;
        document.querySelector('#compose-body').value = `On ${result.timestamp} ${result.sender} wrote: "${result.body}"`;
      })
  }


  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mailbox-content').innerHTML = '';

  // Show the mailbox name
  document.querySelector('#mailbox-title').innerHTML = mailbox.charAt(0).toUpperCase() + mailbox.slice(1);

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(result => {
    result.forEach(email => {
      const box = document.createElement('div');
      box.classList.add('card', 'mb-2', 'p-4', 'email');
      box.addEventListener('click', () => view_email(email.id, mailbox));

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

      const subject = document.createElement('p');
      subject.innerHTML = email.subject;
      subject.classList.add('card-text','pl-2');

      box.append(subject);

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