document.addEventListener('DOMContentLoaded',()=>{
  const form = document.getElementById('todo-form');
  const input = document.getElementById('todo-input');
  const list = document.getElementById('todo-list');
  const themeToggle = document.getElementById('theme-toggle');

  let todos = JSON.parse(localStorage.getItem('todos')||'[]');

  function save(){
    localStorage.setItem('todos', JSON.stringify(todos));
  }

  function render(){
    list.innerHTML = '';
    if(todos.length===0){
      const li = document.createElement('li');
      li.className = 'todo-item';
      li.textContent = 'Nenhuma tarefa. Adicione uma acima.';
      list.appendChild(li);
      return;
    }

    todos.forEach((t, idx)=>{
      const li = document.createElement('li');
      li.className = 'todo-item';

      const left = document.createElement('div');
      left.className = 'todo-left';

      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = t.done;
      cb.addEventListener('change', ()=>{
        t.done = cb.checked;
        save();
        render();
      });

      const span = document.createElement('span');
      span.className = 'todo-text'+(t.done? ' completed':'');
      span.textContent = t.text;

      left.appendChild(cb);
      left.appendChild(span);

      const actions = document.createElement('div');
      actions.className = 'todo-actions';

      const del = document.createElement('button');
      del.type = 'button';
      del.title = 'Remover';
      del.textContent = '✖';
      del.addEventListener('click', ()=>{
        todos.splice(idx,1);
        save();
        render();
      });

      actions.appendChild(del);

      li.appendChild(left);
      li.appendChild(actions);
      list.appendChild(li);
    });
  }

  form.addEventListener('submit',(e)=>{
    e.preventDefault();
    const v = input.value.trim();
    if(!v) return;
    todos.push({text:v,done:false});
    input.value = '';
    save();
    render();
  });

  // theme
  function applyTheme(t){
    if(t==='dark') document.documentElement.setAttribute('data-theme','dark');
    else document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('theme',t);
    themeToggle.textContent = t==='dark'? '☀️':'🌙';
  }

  themeToggle.addEventListener('click', ()=>{
    const cur = localStorage.getItem('theme')||'light';
    applyTheme(cur==='dark'?'light':'dark');
  });

  // init
  const savedTheme = localStorage.getItem('theme')||'light';
  applyTheme(savedTheme);
  render();
});
