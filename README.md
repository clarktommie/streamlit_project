# 🚖 NY Uber Pickups Analysis

An interactive **data science project** exploring Uber pickups in New York City.  
This project combines **Streamlit** for the front-end, **Supabase** for database management, **Modal** for serverless execution, and **uv** for fast Python environment management.

---

## 📊 Project Overview
This project analyzes Uber pickups in New York City, using open datasets to uncover patterns such as:
- Popular pickup times and locations
- Trends across boroughs
- Daily/weekly seasonality
- Demand visualization using heatmaps

The app provides **interactive dashboards** where users can explore these patterns dynamically.

---

## 🛠️ Tech Stack
- **[Streamlit](https://streamlit.io/):** Frontend for interactive visualization  
- **[Supabase](https://supabase.com/):** Backend database for storing data  
- **[Modal](https://modal.com/):** Serverless compute for scalable data pipelines  
- **[uv](https://github.com/astral-sh/uv):** Environment & dependency management  

---

## 📂 Project Structure

---


## Setup Environment with UV
uv venv
uv pip install -r requirements.txt

---


## Create Environment Variables
- SUPABASE_URL=your-supabase-url
- SUPABASE_KEY=your-supabase-key
- MODAL_TOKEN=your-modal-token

---

## run Streamlit script
streamlit run streamlit_run.py

---

🚀 Deployment

Modal: Deploy pipelines or batch jobs using modal deploy.

Streamlit Cloud or Modal: Host the frontend app.

Supabase: Hosts datasets & manages authentication.

📊 Example Visualizations

Heatmap of Uber pickups across NYC

Pickup counts by hour of day

Weekly trends across boroughs

✅ Roadmap

 Add authentication (Supabase Auth)

 Build predictive model for demand forecasting

 Deploy interactive dashboards publicly

 Integrate real-time data pipeline

🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the issues page
.

📜 License

This project is licensed under the MIT License - see the LICENSE
 file for details.
