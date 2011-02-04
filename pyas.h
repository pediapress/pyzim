#include <zim/blob.h>
#include <zim/writer/articlesource.h>
#include <zim/writer/zimcreator.h>

#include <Python.h>

#include <algorithm>


class PyArticle: public zim::writer::Article {
public:
	PyArticle(char ns, const std::string& url, const std::string& title,
		  const std::string& aid, const std::string& redirectAid,
		  const std::string& mimetype)
		: namespace_(ns),
		  url_(url),
		  title_(title),
		  aid_(aid),
		  redirectAid_(redirectAid),
		  mimetype_(mimetype) {
	}

	std::string getAid() const {
		return aid_;
	}

	char getNamespace() const {
		return namespace_;
	}

	std::string getUrl() const {
		return url_;
	}

	std::string getTitle() const {
		return title_;
	}

	bool isRedirect() const {
		return !redirectAid_.empty();
	}

	std::string getMimeType() const {
		return mimetype_;
	}

	bool shouldCompress() const {
		return mimetype_ == "text/html";
	}

	std::string getRedirectAid() const {
		return redirectAid_;
	}

private:
	char namespace_;
	std::string url_;
	std::string title_;
	std::string aid_;
	std::string redirectAid_;
	std::string mimetype_;
	std::string data_;
};


class AidCmp {
public:
	AidCmp(const std::string& aid) : aid_(aid) {}
	bool operator()(const PyArticle* article) {
		return aid_ == article->getAid();
	}

private:
	const std::string& aid_;
};


class PyArticleSource: public zim::writer::ArticleSource {
public:
	typedef PyArticle* (*GetNextArticle)(PyObject* obj);
	typedef std::string (*GetData)(PyObject* obj, std::string aid);

	PyArticleSource(PyObject* pyObj, GetNextArticle getNextArticle, GetData getData)
		: pyObj_(pyObj),
		  getNextArticle_(getNextArticle),
		  getData_(getData),
       		  currentData_("") {
		Py_XINCREF(pyObj_);
	}

	~PyArticleSource() {
		Py_XDECREF(pyObj_);
	}

	virtual const zim::writer::Article* getNextArticle() {
		return getNextArticle_(pyObj_);
	}

	zim::Blob getData(const std::string& aid) {
		currentData_ = getData_(pyObj_, aid);
		return zim::Blob(currentData_.data(), currentData_.length());
	}

private:
	PyObject* pyObj_;
	GetNextArticle getNextArticle_;
	GetData getData_;
	std::string currentData_;
};


void create(const std::string& fname, PyArticleSource* src) {
	int argc = 0;

	try {
		zim::writer::ZimCreator creator(argc, (char**)0);
		creator.create(fname, *src);
	}
	catch (std::exception& e) {
		std::cerr << "exception called:" << e.what() << std::endl;
	}
}
