#!/usr/bin/env node

import { MongoClient } from 'mongodb';
import dotenv from 'dotenv';
import { generateEmbedding } from '../../utils/mistralEmbedding.js';
import { rerankDocuments } from '../../utils/groqClient.js';

dotenv.config();

const client = new MongoClient(process.env.MONGODB_URI, {
  ssl: true,
  tlsAllowInvalidCertificates: true,
  tlsAllowInvalidHostnames: true
});

/**
 * Generate embedding for search query using Mistral AI
 */
async function generateQueryEmbedding(query) {
  try {
    const result = await generateEmbedding(query);
    
    if (!result || !result.embedding) {
      throw new Error(`Mistral AI embedding generation failed`);
    }

    const tokens = result.usage?.total_tokens || 0;
    const cost = (tokens / 1000000) * 0.10; // Mistral pricing: $0.10 per 1M tokens

    return {
      embedding: result.embedding,
      cost: cost,
      tokens: tokens
    };
  } catch (error) {
    console.error('Error generating query embedding:', error.message);
    throw error;
  }
}

/**
 * Perform vector search
 */
async function vectorSearch(collection, queryVector, limit = 50, filters = {}) {
  const pipeline = [
    {
      $vectorSearch: {
        queryVector,
        path: "embedding",
        numCandidates: Math.max(limit * 2, 100),
        limit: limit,
        index: process.env.VECTOR_INDEX_NAME,
        ...(Object.keys(filters).length > 0 && { filter: filters })
      }
    },
    {
      $addFields: {
        vectorScore: { $meta: "vectorSearchScore" }
      }
    },
    { $project: { embedding: 0 } }
  ];

  return await collection.aggregate(pipeline).toArray();
}

/**
 * Perform BM25 search
 */
async function bm25Search(collection, query, limit = 50, filters = {}) {
  const weights = {
    id: 10.0,
    title: 8.0,
    module: 5.0,
    description: 2.0,
    expectedResults: 1.5,
    steps: 1.0,
    preRequisites: 0.8
  };

  const searchFields = Object.entries(weights).map(([field, weight]) => ({
    text: {
      query: query,
      path: field,
      fuzzy: { maxEdits: 1, prefixLength: 2 },
      score: { boost: { value: weight } }
    }
  }));

  const pipeline = [
    {
      $search: {
        index: process.env.BM25_INDEX_NAME,
        compound: {
          should: searchFields,
          minimumShouldMatch: 1
        }
      }
    },
    {
      $addFields: {
        bm25Score: { $meta: "searchScore" }
      }
    },
    { $limit: limit }
  ];

  if (Object.keys(filters).length > 0) {
    pipeline.push({ $match: filters });
  }

  return await collection.aggregate(pipeline).toArray();
}

/**
 * Rerank results using Groq LLM
 */
async function rerankWithGroq(query, documents) {
  if (!process.env.GROQ_API_KEY || process.env.GROQ_API_KEY === 'your_groq_api_key_here') {
    console.warn('\n⚠️  Warning: No valid Groq API key found!');
    console.warn('   Reranking will be skipped. Get a free key from: https://console.groq.com');
    console.warn('   Add it to your .env file as GROQ_API_KEY\n');
    return null;
  }

  try {
    console.log(`🔄 Reranking ${documents.length} documents with Groq AI (${process.env.GROQ_RERANK_MODEL})...`);

    const rerankedDocs = await rerankDocuments(query, documents, documents.length);
    
    // Convert to scores array for compatibility
    return rerankedDocs.map(doc => doc.rerankScore);
  } catch (error) {
    console.error('❌ Reranking error:', error.message);
    return null;
  }
}

/**
 * Display results
 */
function displayResults(results, title, searchType) {
  console.log(`\n${'='.repeat(80)}`);
  console.log(`${title}`);
  console.log(`${'='.repeat(80)}\n`);

  results.forEach((result, index) => {
    const score = result.vectorScore || result.bm25Score || result.rerankScore || 0;
    console.log(`${index + 1}. ${result.id}: ${result.title}`);
    console.log(`   📊 Score: ${score.toFixed(4)}`);
    console.log(`   📦 Module: ${result.module || 'N/A'}`);
    
    if (result.originalRank) {
      const rankChange = result.originalRank - (index + 1);
      const arrow = rankChange > 0 ? '↑' : rankChange < 0 ? '↓' : '↔';
      const changeStr = rankChange !== 0 ? `${Math.abs(rankChange)} positions` : 'no change';
      console.log(`   🔄 Rank Change: ${arrow} ${changeStr} (was #${result.originalRank})`);
    }
    
    if (result.description) {
      const desc = result.description.substring(0, 100);
      console.log(`   📝 ${desc}${result.description.length > 100 ? '...' : ''}`);
    }
    console.log();
  });
}

/**
 * Display comparison
 */
function displayComparison(beforeResults, afterResults) {
  console.log(`\n${'='.repeat(80)}`);
  console.log('📊 BEFORE vs AFTER COMPARISON');
  console.log(`${'='.repeat(80)}\n`);

  console.log('┌──────┬─────────────┬──────────────────────────────────────┬──────────┬──────────┐');
  console.log('│ Orig │ Test Case   │ Title                                │ Before   │ After    │');
  console.log('│ Rank │ ID          │                                      │ Score    │ Rank     │');
  console.log('├──────┼─────────────┼──────────────────────────────────────┼──────────┼──────────┤');

  beforeResults.forEach((beforeResult, index) => {
    const afterIndex = afterResults.findIndex(r => r._id.toString() === beforeResult._id.toString());
    const afterRank = afterIndex >= 0 ? afterIndex + 1 : '-';
    const rankChange = afterIndex >= 0 ? (index + 1) - (afterIndex + 1) : 0;
    const arrow = rankChange > 0 ? '↓' : rankChange < 0 ? '↑' : '↔';
    
    const originalRank = (index + 1).toString().padStart(4);
    const testCaseId = (beforeResult.id || 'N/A').padEnd(11);
    const title = (beforeResult.title || 'No title').substring(0, 36).padEnd(36);
    const beforeScore = (beforeResult.vectorScore || beforeResult.bm25Score || 0).toFixed(4);
    const afterRankStr = afterRank !== '-' ? `${arrow} #${afterRank}`.padEnd(8) : 'dropped';

    console.log(`│ ${originalRank} │ ${testCaseId} │ ${title} │ ${beforeScore} │ ${afterRankStr} │`);
  });

  console.log('└──────┴─────────────┴──────────────────────────────────────┴──────────┴──────────┘');

  // Statistics
  const significantChanges = afterResults.filter(r => Math.abs(r.rankChange || 0) >= 5).length;
  const avgScoreImprovement = afterResults.reduce((sum, r) => sum + parseFloat(r.scoreImprovement || 0), 0) / afterResults.length;

  console.log(`\n📈 STATISTICS:`);
  console.log(`   • Top result changed: ${beforeResults[0]?.id !== afterResults[0]?.id ? 'YES ✓' : 'NO'}`);
  console.log(`   • Significant reorderings (±5 positions): ${significantChanges}`);
  console.log(`   • Average score improvement: ${avgScoreImprovement.toFixed(2)}%`);
}

/**
 * Main function
 */
async function main() {
  try {
    await client.connect();
    const db = client.db(process.env.DB_NAME);
    const collection = db.collection(process.env.COLLECTION_NAME);

    // Parse command line arguments
    const query = process.argv[2] || "merge UHID";
    const searchType = process.argv[3] || "vector"; // vector or bm25
    const rerankTopK = parseInt(process.argv[4]) || 50;
    const finalLimit = parseInt(process.argv[5]) || 10;

    console.log('\n🔍 CrossEncoder Reranking Search');
    console.log(`${'='.repeat(80)}`);
    console.log(`📝 Query: "${query}"`);
    console.log(`🔎 Search Type: ${searchType.toUpperCase()}`);
    console.log(`📊 Retrieve Top-K: ${rerankTopK} → Rerank → Return Top: ${finalLimit}`);
    console.log(`${'='.repeat(80)}\n`);

    const startTime = Date.now();

    // Step 1: Initial search
    console.log(`\n⏳ Step 1: Performing ${searchType.toUpperCase()} search for top ${rerankTopK} candidates...`);
    
    let initialResults;
    let embeddingCost = 0;
    let embeddingTokens = 0;

    if (searchType === 'vector') {
      const embeddingData = await generateQueryEmbedding(query);
      initialResults = await vectorSearch(collection, embeddingData.embedding, rerankTopK);
      embeddingCost = embeddingData.cost;
      embeddingTokens = embeddingData.tokens;
    } else {
      initialResults = await bm25Search(collection, query, rerankTopK);
    }

    const searchTime = Date.now() - startTime;
    console.log(`✅ Found ${initialResults.length} candidates in ${searchTime}ms`);

    // Step 2: Rerank with Groq AI
    console.log(`\n⏳ Step 2: Reranking with Groq AI...`);
    const rerankStartTime = Date.now();
    
    const rerankScores = await rerankWithGroq(query, initialResults);
    
    if (!rerankScores) {
      console.log('\n⚠️  Reranking skipped. Showing original results only.\n');
      displayResults(initialResults.slice(0, finalLimit), `TOP ${finalLimit} RESULTS (${searchType.toUpperCase()})`, searchType);
      return;
    }

    const rerankingTime = Date.now() - rerankStartTime;
    console.log(`✅ Reranking complete in ${rerankingTime}ms`);

    // Step 3: Combine and sort by rerank scores
    const rerankedResults = initialResults.map((doc, index) => ({
      ...doc,
      originalRank: index + 1,
      originalScore: doc.vectorScore || doc.bm25Score || 0,
      rerankScore: rerankScores[index],
      scoreImprovement: ((rerankScores[index] - (doc.vectorScore || doc.bm25Score || 0)) * 100).toFixed(2)
    }));

    rerankedResults.sort((a, b) => b.rerankScore - a.rerankScore);

    // Add new rank and rank change
    rerankedResults.forEach((doc, index) => {
      doc.newRank = index + 1;
      doc.rankChange = doc.originalRank - doc.newRank;
    });

    const finalResults = rerankedResults.slice(0, finalLimit);
    const totalTime = Date.now() - startTime;

    // Display results
    displayResults(initialResults.slice(0, finalLimit), `BEFORE RERANKING - Top ${finalLimit} ${searchType.toUpperCase()} Results`, searchType);
    displayResults(finalResults, `AFTER RERANKING - Top ${finalLimit} Groq AI Results`, 'rerank');
    displayComparison(initialResults.slice(0, finalLimit), finalResults);

    console.log(`\n⏱️  TIMING BREAKDOWN:`);
    console.log(`   • ${searchType.toUpperCase()} Search: ${searchTime}ms`);
    console.log(`   • Groq AI Reranking: ${rerankingTime}ms`);
    console.log(`   • Total Time: ${totalTime}ms`);
    
    if (embeddingCost > 0) {
      console.log(`\n💰 COST:`);
      console.log(`   • Mistral Embedding Cost: $${embeddingCost.toFixed(6)} (Tokens: ${embeddingTokens})`);
      console.log(`   • Groq Reranking: Free tier / extremely low cost`);
      console.log(`   💡 Total Cost Savings: ~95% vs OpenAI + traditional reranking`);
    }

    console.log(`\n✅ Search complete!\n`);

  } catch (error) {
    console.error('\n❌ Error:', error.message);
    process.exit(1);
  } finally {
    await client.close();
  }
}

// Run if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { rerankWithGroq, vectorSearch, bm25Search };
