import React from 'react';
import {
    Card,
    CardContent,
    Typography,
    Box,
    Chip,
    Grid,
    LinearProgress,
    Divider
} from '@mui/material';

const AnalysisResults = ({ results }) => {
    if (!results) {
        return null;
    }

    const {
        sentiment,
        confidence,
        keywords,
        summary,
        entities,
        wordCount,
        readabilityScore
    } = results;

    const getSentimentColor = (sentiment) => {
        switch (sentiment?.toLowerCase()) {
            case 'positive':
                return 'success';
            case 'negative':
                return 'error';
            case 'neutral':
                return 'info';
            default:
                return 'default';
        }
    };

    return (
        <Card elevation={3} sx={{
            width: '100%',
            maxWidth: 800,
            borderRadius: 3,
            background: 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)',
            border: '1px solid rgba(0,0,0,0.1)'
        }}>
            <CardContent sx={{ p: 3 }}>
                <Typography variant="h5" component="h2" gutterBottom sx={{
                    color: '#2c3e50',
                    fontWeight: 'bold',
                    mb: 3
                }}>
                    Analysis Results
                </Typography>

                <Grid container spacing={3}>
                    {/* Sentiment Analysis */}
                    <Grid item xs={12} md={6}>
                        <Box sx={{ mb: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Sentiment Analysis
                            </Typography>
                            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                                <Chip 
                                    label={sentiment || 'Unknown'}
                                    color={getSentimentColor(sentiment)}
                                    variant="filled"
                                    sx={{ fontWeight: 'bold' }}
                                />
                                <Typography variant="body2" color="text.secondary">
                                    Confidence: {confidence ? `${Math.round(confidence * 100)}%` : 'N/A'}
                                </Typography>
                            </Box>
                            {confidence && (
                                <LinearProgress 
                                    variant="determinate" 
                                    value={confidence * 100} 
                                    sx={{ mt: 1, borderRadius: 1 }}
                                    color={getSentimentColor(sentiment)}
                                />
                            )}
                        </Box>
                    </Grid>

                    {/* Text Statistics */}
                    <Grid item xs={12} md={6}>
                        <Box sx={{ mb: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Text Statistics
                            </Typography>
                            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                                {wordCount && (
                                    <Typography variant="body2">
                                        <strong>Word Count:</strong> {wordCount}
                                    </Typography>
                                )}
                                {readabilityScore && (
                                    <Typography variant="body2">
                                        <strong>Readability Score:</strong> {readabilityScore}/100
                                    </Typography>
                                )}
                            </Box>
                        </Box>
                    </Grid>

                    {/* Keywords */}
                    {keywords && keywords.length > 0 && (
                        <Grid item xs={12}>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="h6" gutterBottom>
                                Key Topics
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                {keywords.map((keyword, index) => (
                                    <Chip
                                        key={index}
                                        label={keyword}
                                        variant="outlined"
                                        size="small"
                                        sx={{ borderRadius: 2 }}
                                    />
                                ))}
                            </Box>
                        </Grid>
                    )}

                    {/* Entities */}
                    {entities && entities.length > 0 && (
                        <Grid item xs={12}>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="h6" gutterBottom>
                                Named Entities
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                {entities.map((entity, index) => (
                                    <Chip
                                        key={index}
                                        label={`${entity.text} (${entity.type})`}
                                        color="secondary"
                                        variant="outlined"
                                        size="small"
                                        sx={{ borderRadius: 2 }}
                                    />
                                ))}
                            </Box>
                        </Grid>
                    )}

                    {/* Summary */}
                    {summary && (
                        <Grid item xs={12}>
                            <Divider sx={{ my: 2 }} />
                            <Typography variant="h6" gutterBottom>
                                Summary
                            </Typography>
                            <Typography variant="body1" sx={{
                                backgroundColor: 'rgba(25, 118, 210, 0.04)',
                                padding: 2,
                                borderRadius: 2,
                                border: '1px solid rgba(25, 118, 210, 0.12)'
                            }}>
                                {summary}
                            </Typography>
                        </Grid>
                    )}
                </Grid>
            </CardContent>
        </Card>
    );
};

export default AnalysisResults;