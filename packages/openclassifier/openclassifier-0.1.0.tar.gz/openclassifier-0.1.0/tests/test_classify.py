from openclassifier import OpenClassifier


class TestTextClassify:
    def test_single_label(self, client: OpenClassifier):
        result = client.classify.text(
            "Hello, how are you doing today?",
            ["greeting", "question", "complaint"],
        )
        assert result["success"] is True
        assert "results" in result
        assert result["results"]["label"] in ["greeting", "question", "complaint"]
        assert 0 <= result["results"]["confidence"] <= 1

    def test_multi_label(self, client: OpenClassifier):
        result = client.classify.text(
            "The product is great but shipping was slow",
            ["positive", "negative", "shipping", "product"],
            multi_label=True,
        )
        assert result["success"] is True
        assert "results" in result
        assert isinstance(result["results"], dict)

    def test_sentiment(self, client: OpenClassifier):
        result = client.classify.text(
            "This is the worst experience I've ever had",
            ["positive", "negative", "neutral"],
        )
        assert result["success"] is True
        assert result["results"]["label"] == "negative"


class TestImageClassify:
    def test_image_url(self, client: OpenClassifier):
        result = client.classify.image(
            ["https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg"],
            ["cat", "dog", "bird"],
        )
        assert result["success"] is True
        assert len(result["results"]) == 1
        assert result["results"][0]["label"] == "cat"
        assert 0 <= result["results"][0]["confidence"] <= 1

    def test_multiple_images(self, client: OpenClassifier):
        result = client.classify.image(
            [
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
                "https://upload.wikimedia.org/wikipedia/commons/2/26/YellowLabradorLooking_new.jpg",
            ],
            ["cat", "dog", "bird"],
        )
        assert result["success"] is True
        assert len(result["results"]) == 2


class TestPDFClassify:
    def test_pdf_classification(self, client: OpenClassifier):
        result = client.classify.pdf(
            "https://arxiv.org/pdf/1706.03762.pdf",
            ["research_paper", "invoice", "receipt", "form"],
            aggregation="per_page",
            page_range={"start": 1, "end": 2},
        )
        assert result["success"] is True
        assert "total_pages" in result
        assert "results" in result
        assert len(result["results"]) > 0
        assert result["results"][0]["label"] == "research_paper"
