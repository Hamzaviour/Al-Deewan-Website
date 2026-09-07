const { spawn } = require('child_process');

async function checkProductPage() {
  const chrome = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--headless=new',
    '--remote-debugging-port=9555',
    '--disable-gpu',
    '--window-size=1280,800'
  ]);

  await new Promise(r => setTimeout(r, 1500));

  try {
    const listRes = await fetch('http://127.0.0.1:9555/json');
    const tabs = await listRes.json();
    const pageTab = tabs.find(t => t.type === 'page');
    if (!pageTab) {
      console.log('No page tab');
      chrome.kill();
      return;
    }

    const ws = new WebSocket(pageTab.webSocketDebuggerUrl);
    await new Promise(r => ws.onopen = r);

    let id = 1;
    function send(method, params = {}) {
      return new Promise((resolve) => {
        const curId = id++;
        const handler = (event) => {
          const msg = JSON.parse(event.data);
          if (msg.id === curId) {
            ws.removeEventListener('message', handler);
            resolve(msg.result);
          }
        };
        ws.addEventListener('message', handler);
        ws.send(JSON.stringify({ id: curId, method, params }));
      });
    }

    const errors = [];
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.method === 'Runtime.exceptionThrown') {
        errors.push(msg.params.exceptionDetails);
      }
      if (msg.method === 'Runtime.consoleAPICalled') {
        console.log('[CONSOLE]', msg.params.type, msg.params.args.map(a => a.value));
      }
    });

    await send('Runtime.enable');
    await send('Page.enable');
    await send('Page.navigate', { url: 'http://127.0.0.1:8080/product.html?handle=sapphire-kids-luxury-festive-embroidered-emerald-green-3pc-gharara-suit' });

    await new Promise(r => setTimeout(r, 2500));

    const evalRes = await send('Runtime.evaluate', {
      expression: `(() => {
        return {
          title: document.title,
          pdpTitle: document.getElementById('pdp-title')?.textContent,
          storeExists: typeof Store !== 'undefined',
          catalogExists: typeof CATALOG_PRODUCTS !== 'undefined',
          productCount: typeof Store !== 'undefined' ? (Store.getProducts() || []).length : -1,
          imagesStackHTML: document.getElementById('pdp-images-stack')?.innerHTML.slice(0, 300),
          readyState: document.readyState
        };
      })()`,
      returnByValue: true
    });

    console.log('EVAL RESULT:', JSON.stringify(evalRes.result.value, null, 2));
    if (errors.length > 0) {
      console.log('ERRORS:', JSON.stringify(errors, null, 2));
    } else {
      console.log('No JS runtime exceptions thrown');
    }

    ws.close();
  } catch (e) {
    console.error(e);
  } finally {
    chrome.kill();
  }
}

checkProductPage();
