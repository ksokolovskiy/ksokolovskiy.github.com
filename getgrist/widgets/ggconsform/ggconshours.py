// Импортируем необходимые модули Grist
import {BaseWidget, ConfiguratorTool, GristDocAPI} from '@gristlabs/widget-sdk';

class HoursMoneyForm extends BaseWidget {
  constructor() {
    super();
    this.grist = new GristDocAPI();
  }

  async configure() {
    const config = await ConfiguratorTool.configure({
      hoursTable: ConfiguratorTool.Table,
      moneyTable: ConfiguratorTool.Table,
    });
    return config;
  }

  async buildDom() {
    const form = document.createElement('form');
    form.innerHTML = `
      <label for="client">Client:</label>
      <input type="text" id="client" required>
      <label for="hours">Hours:</label>
      <input type="number" id="hours" required>
      <label for="amount">Amount:</label>
      <input type="number" id="amount" required>
      <button type="submit">Submit</button>
    `;

    form.addEventListener('submit', this.handleSubmit.bind(this));
    this.rootElement.appendChild(form);
  }

  async handleSubmit(event) {
    event.preventDefault();
    const client = document.getElementById('client').value;
    const hours = parseFloat(document.getElementById('hours').value);
    const amount = parseFloat(document.getElementById('amount').value);

    try {
      // Добавляем запись в таблицу Hours
      const hoursRecord = await this.grist.addRecords(this.options.hoursTable, [{
        Client: client,
        Hours: hours
      }]);

      // Добавляем запись в таблицу Money
      await this.grist.addRecords(this.options.moneyTable, [{
        Client: client,
        Amount: amount,
        Hours: hoursRecord[0].id  // Ссылка на запись в таблице Hours
      }]);

      alert('Records added successfully!');
      event.target.reset();
    } catch (error) {
      console.error('Error adding records:', error);
      alert('An error occurred while adding records.');
    }
  }
}

// Регистрируем виджет
BaseWidget.register(HoursMoneyForm);