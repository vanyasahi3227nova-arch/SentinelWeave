using CyberRiskAPI.Models;
using MongoDB.Driver;

namespace CyberRiskAPI.Services
{
    public class CyberRiskService
    {
        private readonly IMongoCollection<CyberRisk> _collection;

        public CyberRiskService(IConfiguration config)
        {
            var settings = config.GetSection("MongoDbSettings").Get<MongoDbSettings>();

            var client = new MongoClient(settings.ConnectionString);
            var database = client.GetDatabase(settings.DatabaseName);

            _collection = database.GetCollection<CyberRisk>(settings.CollectionName);
        }

        // ── Async methods (used by MVC controller) ──────────────────────────

        public async Task<List<CyberRisk>> GetAllAsync() =>
            await _collection.Find(_ => true).ToListAsync();

        public async Task<CyberRisk?> GetByIdAsync(string id) =>
            await _collection.Find(r => r.Id == id).FirstOrDefaultAsync();

        public async Task<CyberRisk> CreateAsync(CyberRisk risk)
        {
            risk.UpdateRiskLevel();
            await _collection.InsertOneAsync(risk);
            return risk;
        }

        public async Task<bool> UpdateAsync(string id, CyberRisk updatedRisk)
        {
            updatedRisk.Id = id;
            updatedRisk.UpdateRiskLevel();

            var result = await _collection.ReplaceOneAsync(r => r.Id == id, updatedRisk);
            return result.ModifiedCount > 0;
        }

        public async Task<bool> DeleteAsync(string id)
        {
            var result = await _collection.DeleteOneAsync(r => r.Id == id);
            return result.DeletedCount > 0;
        }

        // ── Sync methods (kept for any legacy/API usage) ─────────────────────

        public List<CyberRisk> GetAll() =>
            _collection.Find(_ => true).ToList();

        public CyberRisk? GetById(string id) =>
            _collection.Find(r => r.Id == id).FirstOrDefault();

        public CyberRisk Create(CyberRisk risk)
        {
            risk.UpdateRiskLevel();
            _collection.InsertOne(risk);
            return risk;
        }

        public bool Update(string id, CyberRisk updatedRisk)
        {
            updatedRisk.Id = id;
            updatedRisk.UpdateRiskLevel();

            var result = _collection.ReplaceOne(r => r.Id == id, updatedRisk);
            return result.ModifiedCount > 0;
        }

        public bool Delete(string id)
        {
            var result = _collection.DeleteOne(r => r.Id == id);
            return result.DeletedCount > 0;
        }
    }
}