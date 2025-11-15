import { MongoClient } from "mongodb";
import dns from "dns";
import dotenv from "dotenv";
import { generateEmbedding } from "../../utils/mistralEmbedding.js";

dotenv.config();

// Fix DNS resolution issue on macOS by using Google's DNS servers
dns.setServers(['8.8.8.8', '8.8.4.4']);

const client = new MongoClient(process.env.MONGODB_URI);

async function main() {
  try {
    await client.connect();
    const db = client.db(process.env.DB_NAME);
    const collection = db.collection(process.env.COLLECTION_NAME);

    // Take query from command line args, default if missing
    const query = process.argv[2] || "login tests";

    console.log(`🔎 Searching for: "${query}"`);
    console.log(`🔄 Generating embedding with Mistral AI...`);

    // Generate embedding using Mistral AI
    const embeddingResult = await generateEmbedding(query);
    
    if (!embeddingResult || !embeddingResult.embedding) {
      throw new Error(`Mistral AI embedding generation failed`);
    }

    const queryVector = embeddingResult.embedding;
    const tokens = embeddingResult.usage?.total_tokens || 0;
    const cost = (tokens / 1000000) * 0.10; // Mistral pricing: $0.10 per 1M tokens
    
    console.log(`✅ Embedding generated! Cost: $${cost.toFixed(6)}, Tokens: ${tokens}`);

    // Vector search pipeline
    const pipeline = [
      {
        $vectorSearch: {
          queryVector,
          path: "embedding",
          numCandidates: 100,
          limit: 5,
          index: process.env.VECTOR_INDEX_NAME  // must match Atlas Search index name
        }
      },
      {
        $project: {
          testcase_id: 1,
          title: 1,
          description: 1,
          steps: 1,
          expectedResult: 1,
          score: { $meta: "vectorSearchScore" }
        }
      }
    ];

    const results = await collection.aggregate(pipeline).toArray();

    console.log("\n✅ Search results:");
    console.table(results);
    
    console.log(`\n💰 Total Embedding Cost: $${cost.toFixed(6)}`);
    console.log(`📈 Model Used: mistral-embed (Mistral AI)`);
    console.log(`🔢 Results Found: ${results.length}`);
    console.log(`💡 Cost Savings: ~90% cheaper than OpenAI embeddings!`);

  } catch (err) {
    console.error("❌ Error:", err.message);
  } finally {
    await client.close();
  }
}

main();
